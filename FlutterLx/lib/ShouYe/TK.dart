import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutterlx/LianXi/TKXZ.dart';
import 'package:flutterlx/YanShiKuang/ChangYongZhuJian.dart';
import 'package:svg_flutter/svg.dart';

class GRTK extends StatefulWidget {
  GRTK({Key? key}) : super(key: key);

  @override
  _GRTKState createState() => _GRTKState();
}

Widget BT() {
  return Container(
    padding: EdgeInsets.only(left: 16, right: 16),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        YXTZ('lib/assets/images/arrow-left.svg', sss: "退回"),
        Text(
          "题库练习",
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        YXTZ('lib/assets/images/search.svg', sss: "搜索"),
      ],
    ),
  );
}

Widget FLBT() {
  return ListView.separated(
    scrollDirection: Axis.horizontal,
    separatorBuilder: (context, index) {
      return SizedBox(height: 10);
    },
    itemCount: 200,
    itemBuilder: (context, index) {
      return SizedBox(width: 200, child: ListTile(title: Text("第 $index 条数据")));
    },
  );
}
// String? sss;
// Future<void> getData(
//   {String? id}
// ) async {
//   await Dio().get("http://10.42.254.9:8000/getquestion",queryParameters:{"id":id ?? "Q1001"}).then((value) {
//     //  data = value.toString();
//      var data = value.data;
//      var question = data[0];
//      sss = question["title"].toString();
//      print(question["title"]);

//     return value.toString();
//   });

// }

TextEditingController _unameController = TextEditingController();

class _GRTKState extends State<GRTK> {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        children: [
          SizedBox(height: 10),
          BT(),
          SizedBox(height: 10),

          ElevatedButton(
            onPressed: () async {
              // await getData(id: _unameController.text);
              await getQuestions();
              // print(lsitmap.length);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => suatiyemian()),
              );
              setState(() {});
            },
            child: Text("获取数据"),
          ),

          //   Container(
          //   height: 200,
          //   width: double.infinity,
          //   child: SingleChildScrollView(
          //   scrollDirection: Axis.vertical,
          //   child: Text(
          //      sss ?? "",
          //     style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
          //   ),
          // ),
          // ),
          //   SizedBox(height: 10,),

          //          TextField(
          //     autofocus: true,
          //     controller: _unameController , //设置controller
          //     decoration: InputDecoration(
          //       hintText: "请输入题库ID",
          //     ),
          //     onChanged: (value) {
          //       print(_unameController.text);
          //     },
          //  ),
          // SizedBox(
          //     height: 700,
          //     width: 200,
          //      child: FLBT()),

          // SizedBox(height: 10,),
        ],
      ),
    );
  }
}
