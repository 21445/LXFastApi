// import 'package:flutter/material.dart';
// import 'package:flutterlx/DenLu/DL.dart';
// import 'package:flutterlx/YingDaoYe/LunBoTu.dart';
// import 'package:flutterlx/utils/storage.dart';

// /// 启动页 - 用于判断显示引导页还是首页
// class splash_page extends StatefulWidget {
//   splash_page({Key? key}) : super(key: key);

//   @override
//   _splash_pageState createState() => _splash_pageState();
// }

// class _splash_pageState extends State<splash_page> {
//   /// 引导页判断方法 - 根据是否首次打开决定显示引导页或首页
//   Widget YDYPD() {
//     return FutureBuilder<bool>(
//       future: Storage.getIsFirstOpen(), // 获取是否首次打开
//            builder: (context, snapshot) { // 引导页判断方法
//         if (!snapshot.hasData) {// 如果数据为空
//           return Scaffold(body: Center(child: CircularProgressIndicator()));
//         }// 如果数据为空，显示加载中

//         // 第一次打开 → 引导页
//         if (snapshot.data == true) {
//           return SplashPage();
//         } else {
//           // 非第一次 → 首页
//           return DL();
//           // return home_page();
//         }
//       },
//     );
//   }
//   @override
//   Widget build(BuildContext context) {
//     return  YDYPD();
//   }
// }
import 'package:flutter/material.dart';
import 'package:flutterlx/DenLu/DL.dart';
import 'package:flutterlx/YingDaoYe/LunBoTu.dart';
import 'package:flutterlx/utils/storage.dart';

class splash_page extends StatefulWidget {
  splash_page({Key? key}) : super(key: key);

  @override
  _splash_pageState createState() => _splash_pageState();
}

  Widget YDYPD() {
    return FutureBuilder<bool>(
      future: Storage.getIsFirstOpen(), // 获取是否首次打开
           builder: (context, snapshot) { // 引导页判断方法
        if (!snapshot.hasData) {// 如果数据为空
          return Scaffold(body: Center(child: CircularProgressIndicator()));
        }// 如果数据为空，显示加载中
        print("是否首次打开：${snapshot.data}");
        // 第一次打开 → 引导页
        if (snapshot.data == true) {
          return SplashPage();
        } else {
          // 非第一次 → 首页
          return DL();
         
        }
      },
    );
  }
class _splash_pageState extends State<splash_page> {
  @override
  Widget build(BuildContext context) {
    return YDYPD();
  }
}