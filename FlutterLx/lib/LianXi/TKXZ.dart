import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutterlx/LianXi/TKQHLJ.dart';
import 'package:flutterlx/ShouYe/TK.dart';
import 'package:flutterlx/YanShiKuang/ChangYongZhuJian.dart';
import 'package:flutterlx/YanShiKuang/SRK.dart';

class suatiyemian extends StatefulWidget {
  suatiyemian({Key? key}) : super(key: key);

  @override
  _suatiyemianState createState() => _suatiyemianState();
}

String? xuanxiang;

bool isAnswered = false;

Dio dio = Dio(BaseOptions(baseUrl: "http://192.168.22.240:8000"));

String? question = "";
List<String> options = [];
Map<String, dynamic> TIKU = {};
List<Map<String, dynamic>> lsitmap = [];
int currentQuestion = 0;

Future<void> getQuestions() async {
  Response res = await dio.get("/getquestion");

  List<dynamic> data = res.data;
  lsitmap = data.map((e) => e as Map<String, dynamic>).toList();

  // print(res.data);
}

class _suatiyemianState extends State<suatiyemian> {
  // String xuanx = lsitmap[currentQuestion]["correct_answer"].toString();

  Widget XZK({String? XX, String? XZX}) {
    late Color bgColor;
    late Color circleColor;
    late Color borderColor;

    String xuanx = lsitmap[currentQuestion]["correct_answer"].toString();
    if (xuanxiang == null) {
      // 默认状态

      bgColor = Colors.white;
      circleColor = Color.fromARGB(255, 200, 204, 208);
      borderColor = Color.fromARGB(255, 220, 224, 228);
    } else {
      if (XX == xuanxiang) {
        if (XX == xuanx) {
          bgColor = Color.fromARGB(255, 230, 247, 233);
          circleColor = Color.fromARGB(255, 82, 183, 136);
          borderColor = Color.fromARGB(255, 147, 208, 164);
          print("---------------");
          print(XX);
          print(lsitmap[currentQuestion]["correct_answer"].toString());
          print(xuanx);
          print("------------");
        } else {
          bgColor = Color.fromARGB(255, 253, 234, 230);
          circleColor = Color.fromARGB(255, 208, 128, 108);
          borderColor = Color.fromARGB(255, 224, 164, 148);
        }
      } else if (XX == xuanx) {
        bgColor = Color.fromARGB(255, 230, 247, 233);
        circleColor = Color.fromARGB(255, 82, 183, 136);
        borderColor = Color.fromARGB(255, 147, 208, 164);
      } else {
        bgColor = Colors.white;
        circleColor = Color.fromARGB(255, 200, 204, 208);
        borderColor = Color.fromARGB(255, 220, 224, 228);
      }
    }

    return Container(
      height: 60,

      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: borderColor, width: 1),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(10),
          onTap: isAnswered
              ? null
              : () {
                  setState(() {
                    xuanxiang = XX;

                    isAnswered = true; // 点击一次之后锁定答题
                  });
                  print(xuanxiang);
                },
          child: Container(
            padding: EdgeInsets.only(left: 16, right: 16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  height: 30,
                  width: 30,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    color: circleColor,
                  ),
                  child: Text(
                    XX ?? "",
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 20, color: Colors.white),
                  ),
                ),
                SizedBox(width: 10),
                Text(XZX ?? "", style: TextStyle(fontSize: 20)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget DTK() {
    return Container(
      padding: EdgeInsets.only(left: 20, right: 20),
      height: 500,
      width: MediaQuery.of(context).size.width,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: Color.fromRGBO(223, 237, 255, 1), width: 1),
      ),
      child: Column(
        children: [
          SizedBox(height: 10),

          Padding(
            padding: EdgeInsets.only(left: 10, right: 10),
            child: Container(
              // margin: EdgeInsets.only(left: 10, ),
              width: 80,
              height: 20,

              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                color: const Color.fromARGB(255, 141, 205, 205),
              ),
              child: Center(child: Text("单选题", style: TextStyle(fontSize: 15))),
            ),
          ),

          SizedBox(height: 20),
          Container(
            child: Text(
              "${currentQuestion + 1}. ${lsitmap[currentQuestion]["title"] ?? ""}",
              style: TextStyle(fontSize: 18),
            ),
          ),
          SizedBox(height: 40),
          XZK(XX: "A", XZX: lsitmap[currentQuestion]["option_a"]),
          SizedBox(height: 15),
          XZK(XX: "B", XZX: lsitmap[currentQuestion]["option_b"]),
          SizedBox(height: 15),
          XZK(XX: "C", XZX: lsitmap[currentQuestion]["option_c"]),
          SizedBox(height: 15),
          XZK(XX: "D", XZX: lsitmap[currentQuestion]["option_d"]),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFE6F4FF),
      body: SafeArea(
        child: Container(
          padding: EdgeInsets.only(left: 16, right: 16),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              stops: [0.0, 1.0],
              colors: [
                Color.fromRGBO(234, 243, 255, 1),
                Color.fromRGBO(237, 246, 255, 1),
              ],
            ),
          ),

          child: Column(
            children: [
              Container(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    YXTZ('lib/assets/images/arrow-left.svg', sss: "退回"),

                    YXTZ('lib/assets/images/search.svg', sss: "搜索"),
                  ],
                ),
              ),
              SizedBox(height: 30),
              DTK(),

              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                // crossAxisAlignment: CrossAxisAlignment.,
                children: [
                  TextButton(
                    onPressed: () {
                      setState(() {
                        if (currentQuestion == 0) {
                          TSK().XXTC("没有题目了", borderRadius: 15);
                        } else {
                          currentQuestion--;
                          print(lsitmap[currentQuestion]["correct_answer"]);
                          print(lsitmap.length);
                        }
                      });
                    },
                    child: Container(
                      height: currentQuestion == 0 ? 45 : 50,
                      width: 150,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        color: currentQuestion == 0
                            ? Colors.transparent
                            : Color(0xFF90C4E1),
                        border: Border.all(
                          color: Color.fromARGB(255, 188, 230, 252),
                          width: 1,
                        ),
                      ),
                      child: Center(
                        child: Text(
                          "上一题",
                          style: TextStyle(
                            fontSize: 18,
                            color: Color.fromARGB(255, 255, 255, 255),
                          ),
                        ),
                      ),
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      setState(() {
                        xuanxiang = null;
                        isAnswered = false;
                        currentQuestion++;
                      });
                    },
                    child: Container(
                      height: 50,
                      width: 150,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        color: const Color(0xFF90C4E1),
                      ),
                      child: Center(
                        child: Text(
                          "下一题",
                          style: TextStyle(
                            fontSize: 15,
                            color: Color.fromARGB(255, 255, 255, 255),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
