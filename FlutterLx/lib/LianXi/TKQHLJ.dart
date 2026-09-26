// import 'package:dio/dio.dart';

// void main() async {
//   await getQuestions();
// }

// class Question {
//   final String title;
//   final String optionA;
//   final String optionB;
//   final String optionC;
//   final String optionD;
//   final String correctAnswer;
//   final String explanation;
//   final String difficulty;
//   final String category;
//   final String questionId;
//   final int id;

//   Question({
//     required this.title,
//     required this.optionA,
//     required this.optionB,
//     required this.optionC,
//     required this.optionD,
//     required this.correctAnswer,
//     required this.explanation,
//     required this.difficulty,
//     required this.category,
//     required this.questionId,
//     required this.id,
//   });

//   factory Question.fromMap(Map<String, dynamic> map) {
//     return Question(
//       title: map["title"] ?? "",
//       optionA: map["option_a"] ?? "",
//       optionB: map["option_b"] ?? "",
//       optionC: map["option_c"] ?? "",
//       optionD: map["option_d"] ?? "",
//       correctAnswer: map["correct_answer"] ?? "",
//       explanation: map["explanation"] ?? "",
//       difficulty: map["difficulty"] ?? "",
//       category: map["category"] ?? "",
//       questionId: map["question_id"] ?? "",
//       id: map["id"] ?? 0,
//     );
//   }
// }
// List<Map<String, dynamic>> lsitmap = [];

// Dio dio = Dio(
//   BaseOptions(
//     baseUrl: "http://10.42.254.9:8000",
//   ),
// );

//  Future<void> getQuestions() async {
 
//     Response res = await dio.get("/getquestion");
//     List<dynamic> data = res.data;
//     lsitmap = data.map((e) => e as Map<String, dynamic>).toList();
    
//     // print(res.data);
// }

