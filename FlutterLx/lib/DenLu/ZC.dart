// import 'package:flutter/material.dart';

// class AJK extends StatefulWidget {
//   AJK({Key? key}) : super(key: key);

//   @override
//   _AJKState createState() => _AJKState();
// }
// final _formKey = GlobalKey<FormState>();

// Widget DLK() {
//   return Form(
//     key: _formKey,
//     child: Column(
//       children: [
//         TextFormField(
//           decoration: InputDecoration(
//             hintText: '请输入用户名',
//             border: OutlineInputBorder(),
//           ),
//           validator: (value) {
//             if (value == null || value.isEmpty) {
//               return '用户名不能为空';
//             }
//             return null;
//           },
//         ),

//         ElevatedButton(
//           onPressed: () {
//             if (_formKey.currentState!.validate()) {
//               print('校验通过，提交表单');
//             }
//           },
//           child: Text("提交"),
//         ),
//       ],
//     ),
//   );
// }


// class _AJKState extends State<AJK> {
//   @override
//   Widget build(BuildContext context) {
//     return DLK();
//   }
// }