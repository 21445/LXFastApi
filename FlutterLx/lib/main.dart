import 'package:bot_toast/bot_toast.dart';
import 'package:flutter/material.dart';
import 'package:flutterlx/DenLu/DL.dart';
import 'package:flutterlx/DenLu/ZC.dart';
import 'package:flutterlx/ShouYe/SYYD.dart';
import 'package:flutterlx/YingDaoYe/LBTLJ.dart';
import 'package:flutterlx/YingDaoYe/LunBoTu.dart';
import 'package:flutterlx/YingDaoYe/YingDaoYe.dart';

import 'package:flutter/material.dart';
import 'package:flutterlx/YingDaoYe/YingDaoYe.dart';


void main(List<String> args) {
  runApp( CSH()
    );
}

class CSH extends StatefulWidget {
  CSH({Key? key}) : super(key: key);

  @override
  _CSHState createState() => _CSHState();
}

class _CSHState extends State<CSH> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
    builder: BotToastInit(), //1. call BotToastInit
    navigatorObservers: [BotToastNavigatorObserver()],
    // initialRoute: "/SY",
    // routes: {
    //   "/": (context) => DL(),
    //   "/SY": (context) => SY(),
    //   "/CSH": (context) => CSH(),
    // },
    home: splash_page(),
    // home: DL(),
    );
        
      

        
     
      
  }
}