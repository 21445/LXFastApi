import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutterlx/YanShiKuang/SRK.dart';
import 'package:svg_flutter/svg.dart';

class ZYJM extends StatefulWidget {
  ZYJM({Key? key}) : super(key: key);

  @override
  _ZYJMState createState() => _ZYJMState();
}

Widget DB() {
  return Container(
    padding: EdgeInsets.only(left: 16, right: 16),

    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '早上好，同学',
                style: TextStyle(
                  color: Colors.grey,
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                '今天也要加油呀',
                style: TextStyle(
                  color: const Color.fromARGB(255, 55, 55, 55),
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
        Stack(
          children: [
            Container(
              width: 45,
              height: 45,
              padding: EdgeInsets.all(9),
              // color: Colors.grey,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(14),
                color: const Color.fromARGB(255, 255, 253, 253),
              ),
              child: SvgPicture.asset(
                'lib/assets/images/bell.svg',
                width: 10,
                height: 10,
                colorFilter: ColorFilter.mode(Colors.grey, BlendMode.srcATop),
              ),
            ),
            Positioned(
              right: 14,
              top: 8,
              child: Container(
                width: 5,
                height: 5,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(50),
                  color: Colors.red,
                ),
              ),
            ),
          ],
        ),
      ],
    ),
  );
}

final GlobalKey<FormState> _SSKFormKey = GlobalKey<FormState>();
final TextEditingController _SSKController = TextEditingController();

Widget SSK(){
  return Container(
    height: 50,
    padding: EdgeInsets.only(left: 16, right: 16),
    child: TextFormField(
      key: _SSKFormKey,
      textAlignVertical: TextAlignVertical.center, //文字垂直居中
      style: const TextStyle(fontSize: 15, color: Color.fromARGB(205, 8, 8, 8)),
      maxLines: 1,
      inputFormatters: [LengthLimitingTextInputFormatter(15)],
      obscureText: false,
      controller: _SSKController,

      decoration: InputDecoration(
        isDense: true, //紧凑模式
        floatingLabelAlignment: FloatingLabelAlignment.center,
        hintText: "搜索",
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        errorStyle: const TextStyle(height: 0, fontSize: 0),
        hintStyle: const TextStyle(color: Colors.grey, fontSize: 14),
        filled: true,

        fillColor: const Color.fromARGB(255, 255, 255, 255),
        suffixIcon: IconButton(
          padding: EdgeInsets.zero, //清除IconButton默认边距
          constraints: BoxConstraints(minWidth: 24, minHeight:24),
          icon: SvgPicture.asset(
            'lib/assets/images/sliders-horizontal.svg',
            colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),
          ),
          onPressed: () {
            print("设置");
          },
        ),

        prefixIcon: IconButton(
          padding: EdgeInsets.zero, //清除IconButton默认边距
          constraints: BoxConstraints(minWidth:24, minHeight:24),
          icon: SvgPicture.asset(
            'lib/assets/images/search.svg',
            colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),
          ),
          onPressed: () {
            if(_SSKController.text.isNotEmpty){
              print("搜索${_SSKController.text}");
            }
          },
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: const Color.fromARGB(255, 139, 200, 204), width: 2),
        ),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return "";
        }
        return null;
      },
    ),
  );
}

Widget XXQKZS() {
  return Padding(
    padding: EdgeInsets.symmetric(horizontal: 16),
    child: Container(
      height: 150,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        gradient: LinearGradient(
          begin: Alignment.centerLeft, // 起点：左边
          end: Alignment.centerRight, // 终点：右边
          colors: [
            Color(0xff96d2ee), // 左边浅蓝
            Color(0xffc7eed8), // 右边淡薄荷绿
          ],
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Padding(
            padding: EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: EdgeInsets.symmetric(horizontal:12, vertical:6),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text("今日目标", style: TextStyle(color: Colors.white)),
                ),
                SizedBox(height:10),
                Text("科学刷题", style: TextStyle(color: Colors.white, fontSize:19, fontWeight: FontWeight.bold)),
                Text("高效备考", style: TextStyle(color: Colors.white, fontSize:19, fontWeight: FontWeight.bold)),
                SizedBox(height:7),
                Text("已完成 42 / 80 题", style: TextStyle(color: Colors.white, fontSize:15)),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

// 顶部三个统计卡片组件
Widget _buildStatCard(String num,String title){
  return Container(
    padding: EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(10),
    ),
    child: Column(
      children: [
        Text(num,style: TextStyle(fontSize:24,fontWeight: FontWeight.bold,color: Color(0xff60a8d8))),
        SizedBox(height:4),
        Text(title,style: TextStyle(fontSize:13,color:Colors.grey)),
      ],
    ),
  );
}

//快捷功能Item
Widget _buildFuncItem({required Widget icon, required String title}){
  return Container(
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(10),
    ),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        icon,
        SizedBox(height:8),
        Text(title,style: TextStyle(fontSize:14)),
      ],
    ),
  );
}

//继续上次练习卡片
Widget _buildContinueCard(){
  return Padding(
    padding: EdgeInsets.symmetric(horizontal:16),
    child: Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          SvgPicture.asset("lib/assets/images/book.svg",width:32),
          SizedBox(width:12),
          Expanded(child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("继续上次练习",style: TextStyle(color:Colors.grey,fontSize:13)),
              Text("高等数学·第3章",style: TextStyle(fontSize:16,fontWeight: FontWeight.bold)),
              Text("剩余18题·预计12分钟",style: TextStyle(fontSize:13,color:Colors.grey)),
            ],
          )),
          TextButton(onPressed: (){}, child: Text("继续",style: TextStyle(color: Color(0xff60a8d8)))),
        ],
      ),
    ),
  );
}

class _ZYJMState extends State<ZYJM> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xfff2f6fa), //页面背景浅灰蓝
      body: SingleChildScrollView( //外层滚动，解决GridView报错
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height:40),
            DB(),
            SizedBox(height: 16),
            SSK(),
            SizedBox(height: 16),
            XXQKZS(),
            SizedBox(height:16),
            // 顶部3个统计卡片
            Padding(
              padding: EdgeInsets.symmetric(horizontal:16),
              child: Row(
                children: [
                  Expanded(child: _buildStatCard("126","连续天数")),
                  SizedBox(width:12),
                  Expanded(child: _buildStatCard("87%","平均正确率")),
                  SizedBox(width:12),
                  Expanded(child: _buildStatCard("2480","累计刷题")),
                ],
              ),
            ),
            SizedBox(height:20),
            //快捷功能标题
            Padding(
              padding: EdgeInsets.symmetric(horizontal:16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text("快捷功能",style: TextStyle(fontSize:18,fontWeight: FontWeight.bold)),
                  TextButton(onPressed: (){}, child: Text("全部 >",style: TextStyle(color:Colors.grey))),
                ],
              ),
            ),
            SizedBox(height:12),
            //快捷功能网格 GridView.count
            Padding(
              padding: EdgeInsets.symmetric(horizontal:16),
              child: GridView.count(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                crossAxisCount:3,
                crossAxisSpacing:12,
                mainAxisSpacing:12,
                children: [
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/zap.svg",width:28,colorFilter: ColorFilter.mode(Color(0xff52b8e8),BlendMode.srcIn)), title:"智能刷题"),
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/library.svg",width:28,colorFilter: ColorFilter.mode(Color(0xff799fd8),BlendMode.srcIn)), title:"题库选择"),
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/list-checks.svg",width:28,colorFilter: ColorFilter.mode(Color(0xffd89888),BlendMode.srcIn)), title:"章节练习"),
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/timer.svg",width:28,colorFilter: ColorFilter.mode(Color(0xff86d2a8),BlendMode.srcIn)), title:"模拟考试"),
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/alert-circle.svg",width:28,colorFilter: ColorFilter.mode(Color(0xffe6c285),BlendMode.srcIn)), title:"错题本"),
                  _buildFuncItem(icon:SvgPicture.asset("lib/assets/images/bookmark.svg",width:28,colorFilter: ColorFilter.mode(Color(0xffdd9fc2),BlendMode.srcIn)), title:"我的收藏"),
                ],
              ),
            ),
            SizedBox(height:20),
            //继续上次练习卡片
            _buildContinueCard(),
            SizedBox(height:30),
          ],
        ),
      ),
    );
  }
}