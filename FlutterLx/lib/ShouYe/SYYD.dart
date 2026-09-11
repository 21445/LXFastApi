import 'package:flutter/material.dart';
import 'package:flutterlx/ShouYe/ZY.dart';
import 'package:svg_flutter/svg.dart';

class SY extends StatefulWidget {
  SY({Key? key}) : super(key: key);

  @override
  _SYState createState() => _SYState();
}
int currentIndex = 0;
Widget _buildPageContent() {
    switch (currentIndex) {
      case 0:
        return ZYJM(); //首页，显示ZYJM
      case 1:
        return Container(child: Center(child: Text("题库页面")));
      case 2:
        return Container(child: Center(child: Text("练习页面")));
      case 3:
        return Container(child: Center(child: Text("我的页面")));
      default:
        return ZYJM();
    }
  }

class _SYState extends State<SY> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFE6F4FF), 
     body:SafeArea(
      
        child: Container(
          decoration: BoxDecoration(
           gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              stops: [0.0, 1.0],
              colors: [
                Color.fromRGBO(234, 243, 255, 1),
                Color(0xFFFFFFFF),
              ],
            ),
        ),
        child: _buildPageContent(),
        ),
     ),
     bottomNavigationBar: BottomNavigationBar(
       selectedItemColor: Color(0xff90c4e1), //选中文字颜色
        unselectedItemColor: Colors.grey, //未选中文字
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        // 取消按压底色，只保留水波纹
        showSelectedLabels: true, // 选中文字显示
        showUnselectedLabels: true,
       items: [
         BottomNavigationBarItem(
           icon: SvgPicture.asset(
            "lib/assets/images/home.svg",
            width: 24,height: 24,
            colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
           label: "首页",
           activeIcon: SvgPicture.asset(
            "lib/assets/images/home.svg",
            width: 24,height: 24,
            colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
         ),
         BottomNavigationBarItem(
           icon: SvgPicture.asset("lib/assets/images/library.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
           label: "题库",
           activeIcon: SvgPicture.asset(
            "lib/assets/images/library.svg",
            width: 24,height: 24,
            colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
         ),
         BottomNavigationBarItem(
           icon: SvgPicture.asset("lib/assets/images/pencil.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
           label: "练习",
           activeIcon: SvgPicture.asset(
            "lib/assets/images/pencil.svg",
            width: 24,height: 24,
            colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
         ),
         BottomNavigationBarItem(
           icon: SvgPicture.asset("lib/assets/images/user.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
           label: "我的",
           
           activeIcon: SvgPicture.asset(
            "lib/assets/images/user.svg",
            width: 24,height: 24,
            colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
         ),
       ],
       currentIndex: currentIndex, // 当前选中的是第几个 tab，从 0 开始
       onTap: (index) {
         setState(() {
           currentIndex = index;
         });
       },
     ),
    );
  }
}