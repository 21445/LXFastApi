import 'package:flutter/material.dart';
import 'package:svg_flutter/svg.dart';

class CYZJ extends StatefulWidget {
  CYZJ({Key? key}) : super(key: key);

  @override
  _CYZJState createState() => _CYZJState();
}
Widget YXTZ(
  String imsgr,
  {String? sss,
  
  }
 ) {
  return Container(
    width: 45,
    height: 45,
    padding: EdgeInsets.all(9),
    // color: Colors.grey,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(14),
      color: const Color.fromARGB(255, 255, 253, 253),
    ),
    child: Material(
      color: const Color.fromARGB(0, 193, 190, 190),
      child: InkWell(
        onTap: () {
          print("输出了$sss");
        },
        borderRadius: BorderRadius.circular(14),
        child: SvgPicture.asset(
          imsgr ,
          width: 10,
          height: 10,
          colorFilter: ColorFilter.mode(Colors.grey, BlendMode.srcATop),
        ),
      ),
    ),
  );
}

Widget Kuang( String num,String title){
  return  
     Container(
    padding: EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(10),
       border: Border.all(color: Color.fromRGBO(223, 237, 255, 1), width: 1),
    ),
    child: Material(
    color: const Color.fromARGB(0, 204, 7, 7),
    
    child: InkWell(
      borderRadius: BorderRadius.circular(10),
    onTap: (){
      print(title);
    },
    child:Text("$num",style: TextStyle(fontSize:24,fontWeight: FontWeight.bold,color: Color(0xff60a8d8))),
    ),
     
  ),
     );
}
class _CYZJState extends State<CYZJ> {
  @override
  Widget build(BuildContext context) {
    return Container(
       child: null,
    );
  }
}