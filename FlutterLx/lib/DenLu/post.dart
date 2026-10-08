import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb, defaultTargetPlatform, TargetPlatform;

import 'package:crypto/crypto.dart';

class Post {

  // final String phone;
  // final String password;
  final int code;
  final String? error;
  final String? token;
  

  const Post({
    // required this.id,
    // required this.userId,
    // required this.phone,
    // required this.password,
    required this.code,
    this.error,
    this.token,
  });

  factory Post.fromJson(Map<String, dynamic> json) => Post(
        // id: (json['id'] as num).toInt(),
        // userId: (json['userId'] as num).toInt(),
        // phone: json['phone'] as String,
        // password: json['password'] as String,
        code: json['code'] as int,
        error: json['error'] as String?,
        token: json['token'] as String?,
      );
}

class Md5  {
  String generateMd5(String input) {
    List<int> bytes = utf8.encode(input);
    Digest md5Result = md5.convert(bytes);
    return md5Result.toString();
}
}

// 获取当前平台名称
String getPlatformName() {
  if (kIsWeb) {
    return "web";
  }
  switch(defaultTargetPlatform){
    case TargetPlatform.android:
      return "android";
    case TargetPlatform.iOS:
      return "ios";
    case TargetPlatform.windows:
      return "windows";
    case TargetPlatform.macOS:
      return "macos";
    case TargetPlatform.linux:
      return "linux";
    default:
      return "unknown";
  }
}
