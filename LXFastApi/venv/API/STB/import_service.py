# -*- coding: utf-8 -*-
"""题库导入的数据库层。

流程：
    1. 上传文件 → 解析 → 落 ImportTask / ImportFile / ImportItem（待确认）
    2. 人工确认 → 把 ImportItem 写入 Question / QuestionOption / Chapter

说明：ImportItem 没有 chapter / score 字段，这些附加信息统一放在 options_json 里，
形如 {"options": [...], "chapter": "第一章", "score": 2, "knowledge": null}。
"""

import os
import re
from datetime import datetime

from parse_common import normalize_judge_answer
from tortoise_models import (
    Bank,
    Chapter,
    ImportFile,
    ImportItem,
    ImportTask,
    Question,
    QuestionOption,
    Subject,
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

DEFAULT_SUBJECT_NAME = "默认科目"
DEFAULT_SUBJECT_CODE = "default"

VALID_ITEM_STATUS = ("pending", "confirmed", "rejected")


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return UPLOAD_DIR


async def get_subject(subject_id=None):
    """取指定科目；不传或找不到时回退到默认科目（没有就创建）。"""
    if subject_id:
        subject = await Subject.get_or_none(id=subject_id)
        if subject is not None:
            return subject
    subject = await Subject.get_or_none(code=DEFAULT_SUBJECT_CODE)
    if subject is None:
        subject = await Subject.create(
            name=DEFAULT_SUBJECT_NAME, code=DEFAULT_SUBJECT_CODE, sort=0, status=1
        )
    return subject


async def save_upload_file(upload_file):
    """把上传文件落盘，返回 (保存路径, 原始文件名, 落盘文件名, 后缀, 字节数)。"""
    ensure_upload_dir()
    filename = os.path.basename(upload_file.filename or "upload")
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    stored_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
    path = os.path.join(UPLOAD_DIR, stored_name)
    content = await upload_file.read()
    with open(path, "wb") as f:
        f.write(content)
    return path, filename, stored_name, ext, len(content)


async def create_import_task(user_id, bank_name, subject_id, filename, stored_name, ext,
                             file_size, items, meta):
    """新建题库 + 导入任务，并把解析结果写为待确认明细。"""
    subject = await get_subject(subject_id)
    bank = await Bank.create(
        subject_id=subject.id,
        name=(bank_name or os.path.splitext(filename)[0])[:64],
        bank_type="custom",
        visibility="private",
        question_count=0,
        chapter_count=0,
        status=1,
    )

    now = datetime.now()
    task = await ImportTask.create(
        user_id=user_id,
        bank_id=bank.id,
        source_type=ext[:16],
        engine="local",
        file_count=1,
        status="parsed",
        progress=100,
        total_count=len(items),
        started_at=now,
        finished_at=now,
    )
    import_file = await ImportFile.create(
        task_id=task.id,
        file_name=filename[:128],
        file_ext=ext[:8],
        file_size=file_size,
        storage_url=stored_name[:255],
        page_count=meta.get("page_count") or 0,
        ocr_status="done",
    )

    confidence = meta.get("confidence", 0)
    rows = []
    for i, item in enumerate(items, start=1):
        rows.append(
            ImportItem(
                task_id=task.id,
                file_id=import_file.id,
                seq=i,
                q_type=(item.get("q_type") or None),
                stem=item.get("stem"),
                options_json={
                    "options": item.get("options") or [],
                    "chapter": item.get("chapter"),
                    "score": item.get("score"),
                    "knowledge": item.get("knowledge"),
                },
                answer=(item.get("answer") or None),
                analysis=item.get("analysis"),
                confidence=confidence,
                status="pending",
            )
        )
    if rows:
        await ImportItem.bulk_create(rows)

    return task, bank


def item_to_dict(item):
    payload = item.options_json or {}
    return {
        "id": item.id,
        "seq": item.seq,
        "q_type": item.q_type,
        "stem": item.stem,
        "options": payload.get("options") or [],
        "answer": item.answer,
        "analysis": item.analysis,
        "chapter": payload.get("chapter"),
        "score": payload.get("score"),
        "knowledge": payload.get("knowledge"),
        "confidence": float(item.confidence or 0),
        "status": item.status,
        "question_id": item.question_id,
    }


async def _get_or_create_chapter(bank, path, cache):
    name = (path or "").strip()[:64] or "未分类"
    if name in cache:
        return cache[name]
    chapter = await Chapter.get_or_none(bank_id=bank.id, name=name)
    if chapter is None:
        last = await Chapter.filter(bank_id=bank.id).order_by("-seq").first()
        next_seq = (last.seq + 1) if last else 1
        chapter = await Chapter.create(bank_id=bank.id, name=name, seq=next_seq, status=1)
    cache[name] = chapter
    return chapter


def _correct_labels(q_type, answer, options):
    """算出哪些选项是正确答案。"""
    answer = (answer or "").strip()
    labels = {(o.get("label") or "").upper() for o in options}
    if not labels:
        return set()
    if q_type == "判断题":
        judge = normalize_judge_answer(answer)
        if judge == "正确" and "A" in labels:
            return {"A"}
        if judge == "错误" and "B" in labels:
            return {"B"}
    letters = set(re.findall(r'[A-Ja-j]', answer.upper()))
    return {letter for letter in letters if letter in labels}


async def _create_options(question, item):
    payload = item.options_json or {}
    options = payload.get("options") or []
    if not options:
        return
    correct = _correct_labels(item.q_type, item.answer, options)
    rows = []
    for index, option in enumerate(options):
        label = (option.get("label") or "").strip()[:4]
        if not label:
            continue
        rows.append(
            QuestionOption(
                question_id=question.id,
                label=label,
                content=(option.get("content") or "")[:500],
                is_correct=1 if label.upper() in correct else 0,
                sort=index,
            )
        )
    if rows:
        await QuestionOption.bulk_create(rows)


async def confirm_import(task_id, item_ids=None):
    """把待确认的解析明细真正写入题库，返回入库题目数。"""
    task = await ImportTask.get_or_none(id=task_id)
    if task is None:
        raise ValueError("导入任务不存在")

    query = ImportItem.filter(task_id=task_id, status="pending").order_by("seq")
    if item_ids:
        query = query.filter(id__in=item_ids)
    items = await query
    if not items:
        raise ValueError("没有待确认的题目")

    bank = await Bank.get(id=task.bank_id)
    chapter_cache = {}
    created = 0
    for item in items:
        payload = item.options_json or {}
        chapter = None
        if payload.get("chapter"):
            chapter = await _get_or_create_chapter(bank, payload["chapter"], chapter_cache)
        question = await Question.create(
            bank_id=bank.id,
            chapter_id=chapter.id if chapter else None,
            q_type=(item.q_type or "单选题")[:16],
            stem=item.stem or "",
            answer=(item.answer or "")[:255],
            analysis=item.analysis,
            score=payload.get("score") or 1,
            status=1,
        )
        await _create_options(question, item)
        item.status = "confirmed"
        item.question_id = question.id
        await item.save()
        created += 1

    await ImportTask.filter(id=task.id).update(
        confirmed_count=(task.confirmed_count or 0) + created,
        status="confirmed",
        finished_at=datetime.now(),
    )
    await Bank.filter(id=bank.id).update(
        question_count=(bank.question_count or 0) + created,
        chapter_count=await Chapter.filter(bank_id=bank.id).count(),
    )
    return created


async def reject_items(task_id, item_ids=None):
    """把待确认明细标记为已忽略，返回条数。"""
    query = ImportItem.filter(task_id=task_id, status="pending")
    if item_ids:
        query = query.filter(id__in=item_ids)
    return await query.update(status="rejected")