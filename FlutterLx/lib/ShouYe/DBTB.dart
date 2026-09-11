// import 'package:flutter/material.dart';
// import 'package:svg_flutter/svg.dart';

// class DBTB{
//   // static Widget TB (
//     int currentIndex,
//     Function(int index) sbh,
//     List<BottomNavigationBarItem> items ,
//   ){
//      return BottomNavigationBar (


//       selectedItemColor: Color(0xff90c4e1), //选中文字颜色
//         unselectedItemColor: Colors.grey, //未选中文字
//         type: BottomNavigationBarType.fixed,
//         backgroundColor: Colors.white,
//         // 取消按压底色，只保留水波纹
//         // showSelectedLabels: true, // 选中文字显示
//         // showUnselectedLabels: true, // 未选中文字显示
//         items: items,
//        items: [
//          BottomNavigationBarItem(
//            icon: SvgPicture.asset(
//             "lib/assets/images/home.svg",
//             width: 24,height: 24,
//             colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
//            label: "首页",
//            activeIcon: SvgPicture.asset(
//             "lib/assets/images/home.svg",
//             width: 24,height: 24,
//             colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
//          ),
//          BottomNavigationBarItem(
//            icon: SvgPicture.asset("lib/assets/images/library.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
//            label: "题库",
//            activeIcon: SvgPicture.asset(
//             "lib/assets/images/library.svg",
//             width: 24,height: 24,
//             colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
//          ),
//          BottomNavigationBarItem(
//            icon: SvgPicture.asset("lib/assets/images/pencil.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
//            label: "练习",
//            activeIcon: SvgPicture.asset(
//             "lib/assets/images/pencil.svg",
//             width: 24,height: 24,
//             colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
//          ),
//          BottomNavigationBarItem(
//            icon: SvgPicture.asset("lib/assets/images/user.svg",width: 24,height: 24,colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),),
//            label: "我的",
           
//            activeIcon: SvgPicture.asset(
//             "lib/assets/images/user.svg",
//             width: 24,height: 24,
//             colorFilter: const ColorFilter.mode(Color(0xff90c4e1), BlendMode.srcIn),),
//          ),
//        ],
//        currentIndex: currentIndex, // 当前选中的是第几个 tab，从 0 开始
//        onTap: sbh,
       
     
     
//      );
       
//   }

// }