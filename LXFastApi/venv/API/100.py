import os
from modelscope.hub.snapshot_download import snapshot_download

model_id = "Comfy-Org/MiniMax-H3"
save_dir = r"E:\UI"

model_dir = snapshot_download(
    model_id=model_id,
    local_dir=save_dir,
    allow_patterns=[

        "text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors",
     
    ]
)

print(f"✅ 下载完成：{model_dir}")