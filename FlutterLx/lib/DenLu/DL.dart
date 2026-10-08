import 'package:bot_toast/bot_toast.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutterlx/DenLu/post.dart';
import 'package:flutterlx/YanShiKuang/SRK.dart';
import 'package:flutterlx/ShouYe/SYYD.dart';
import 'package:svg_flutter/svg.dart';
// 确认md5导入

class DL extends StatefulWidget {
  DL({Key? key}) : super(key: key);
  @override
  _DLState createState() => _DLState();
}

class _DLState extends State<DL> {
  bool isLogin = false;
  // 验证码倒计时
  bool _codeBtnDisable = false;
  int _countDown = 0;

  // ========= 登录表单 =========
  final GlobalKey<FormState> _loginFormKey = GlobalKey<FormState>();
  final TextEditingController _loginEmailCtrl = TextEditingController();
  final TextEditingController _loginPwdCtrl = TextEditingController();
  // ========= 注册表单 =========
  final GlobalKey<FormState> _registerFormKey = GlobalKey<FormState>();
  final TextEditingController _regEmailCtrl = TextEditingController();
  final TextEditingController _regPwdCtrl = TextEditingController();
  final TextEditingController _regConfirmPwdCtrl = TextEditingController();
  final TextEditingController _regCodeCtrl = TextEditingController();
  final TSK _tsk = TSK();

  // 倒计时定时器
  void _startCountDown() {
    setState(() {
      _codeBtnDisable = true;
      _countDown = 60;
    });
    Future.doWhile(() async {
      await Future.delayed(const Duration(seconds: 1));
      if (_countDown <= 1) {
        setState(() {
          _codeBtnDisable = false;
          _countDown = 0;
        });
        return false;
      }
      setState(() {
        _countDown--;
      });
      return true;
    });
  }

  Widget HYJM() {
    return Container(
      padding: EdgeInsets.only(top: 100),
      alignment: Alignment.center,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Container(
            padding: EdgeInsets.all(10),
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              color: Color.fromARGB(255, 149, 198, 225),
              borderRadius: BorderRadius.circular(15),
            ),
            child: SvgPicture.asset(
              "lib/assets/images/book-open-check.svg",
              width: 20,
              height: 20,
              color: Colors.white,
            ),
          ),
          SizedBox(height: 20),
          Text(
            "欢迎来到刷题宝",
            style: TextStyle(
              fontSize: 25,
              color: Colors.black,
              fontWeight: FontWeight.w600,
            ),
          ),
          SizedBox(height: 10),
          Text(
            "登录同步刷题和考试记录",
            style: TextStyle(
              fontSize: 20,
              color: Colors.grey,
              fontWeight: FontWeight.w600,
            ),
          ),
          SizedBox(height: 20),
          Container(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                TextButton(
                  onPressed: () {
                    setState(() {
                      isLogin = true;
                      //切换清空数据
                      _loginFormKey.currentState?.reset();
                      _registerFormKey.currentState?.reset();
                      _loginEmailCtrl.clear();
                      _loginPwdCtrl.clear();
                      _regEmailCtrl.clear();
                      _regPwdCtrl.clear();
                      _regConfirmPwdCtrl.clear();
                      _regCodeCtrl.clear();
                      print("登录");
                    });
                  },
                  child: Text(
                    "登录",
                    style: TextStyle(
                      fontSize: 20,
                      color: isLogin
                          ? Color.fromARGB(255, 149, 198, 225)
                          : Colors.grey,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    setState(() {
                      isLogin = false;
                      _loginFormKey.currentState?.reset();
                      _registerFormKey.currentState?.reset();
                      _loginEmailCtrl.clear();
                      _loginPwdCtrl.clear();
                      _regEmailCtrl.clear();
                      _regPwdCtrl.clear();
                      _regConfirmPwdCtrl.clear();
                      _regCodeCtrl.clear();
                      // 切换注册页重置倒计时
                      _codeBtnDisable = false;
                      _countDown = 0;
                      print("注册");
                    });
                  },
                  child: Text(
                    "注册",
                    style: TextStyle(
                      fontSize: 20,
                      color: isLogin
                          ? Colors.grey
                          : Color.fromARGB(255, 149, 198, 225),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: 5, left: 50, right: 50),
            width: double.infinity,
            height: 3,
            decoration: BoxDecoration(
              color: const Color.fromARGB(205, 221, 221, 221),
              borderRadius: BorderRadius.circular(30),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                AnimatedContainer(
                  duration: Duration(milliseconds: 200),
                  width: MediaQuery.of(context).size.width / 2 - 55,
                  height: 3,
                  color: isLogin
                      ? Color.fromARGB(255, 149, 198, 225)
                      : const Color.fromARGB(205, 221, 221, 221),
                ),
                SizedBox(width: 5),
                AnimatedContainer(
                  duration: Duration(milliseconds: 200),
                  width: MediaQuery.of(context).size.width / 2 - 55,
                  height: 3,
                  color: isLogin
                      ? const Color.fromARGB(205, 221, 221, 221)
                      : Color.fromARGB(255, 149, 198, 225),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  //登录表单
  Widget DLK() {
    return Container(
      padding: EdgeInsets.only(top: 20, left: 50, right: 50),
      child: Form(
        key: _loginFormKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClassName.TSC("邮箱", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _loginEmailCtrl,
                svgPath: "lib/assets/images/phone.svg",
                hintText: "请输入邮箱",
                maxLength: 64,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return " ";
                  }
                  return null;
                },
              ),
            ),
            SizedBox(height: 8),
            ClassName.TSC("密码", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _loginPwdCtrl,
                svgPath: "lib/assets/images/lock.svg",
                hintText: "请输入密码",
                maxLength: 13,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return " ";
                  }
                  return null;
                },
                obscureText: true,
              ),
            ),
            SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  //注册表单
  //注册表单
  Widget ZCK() {
    return Container(
      padding: EdgeInsets.only(top: 20, left: 50, right: 50),
      child: Form(
        key: _registerFormKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClassName.TSC("邮箱", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _regEmailCtrl,
                svgPath: "lib/assets/images/phone.svg",
                hintText: "请输入邮箱",
                maxLength: 64,
                validator: (value) {
                  if (value == null || value.isEmpty) return " ";
                  return null;
                },
              ),
            ),
            SizedBox(height: 8),
            ClassName.TSC("密码", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _regPwdCtrl,
                svgPath: "lib/assets/images/lock.svg",
                hintText: "请输入密码",
                maxLength: 13,
                validator: (value) {
                  if (value == null || value.isEmpty) return " ";
                  return null;
                },
                obscureText: true,
              ),
            ),
            SizedBox(height: 8),
            ClassName.TSC("确认密码", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _regConfirmPwdCtrl,
                svgPath: "lib/assets/images/lock.svg",
                hintText: "请输入确认密码",
                maxLength: 13,
                validator: (value) {
                  if (value == null || value.isEmpty) return " ";
                  return null;
                },
                obscureText: true,
              ),
            ),
            SizedBox(height: 8),
            ClassName.TSC("验证码", FontWeight.w600),
            SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: Container(
                    height: 50,
                    child: ClassName.srk(
                      controller: _regCodeCtrl,
                      svgPath: "lib/assets/images/lock.svg",
                      hintText: "请输入验证码",
                      maxLength: 6,
                      validator: (value) {
                        if (value == null || value.isEmpty) return " ";
                        return null;
                      },
                    ),
                  ),
                ),
                SizedBox(width: 25),
                Container(
                  padding: EdgeInsets.only(right: 10),
                  child: TextButton(
                    onPressed: _codeBtnDisable
                        ? null
                        : () async {
                            String email = _regEmailCtrl.text.trim();
                            String pwd = _regPwdCtrl.text.trim();
                            String confirmPwd = _regConfirmPwdCtrl.text.trim();
                            // 校验邮箱
                            if (email.isEmpty) {
                              _tsk.XXTC("请先输入邮箱", onlyOne: true);
                              return;
                            }
                            if (!RegExp(
                              r'^[\w.+-]+@[\w-]+\.[\w.-]+$',
                            ).hasMatch(email)) {
                              _tsk.XXTC("邮箱格式不正确", onlyOne: true);
                              return;
                            }
                            // 校验密码
                            if (pwd.isEmpty) {
                              _tsk.XXTC("请先填写密码", onlyOne: true);
                              return;
                            }
                            // 校验确认密码
                            if (confirmPwd.isEmpty) {
                              _tsk.XXTC("请先填写确认密码", onlyOne: true);
                              return;
                            }

                            var _sendEmailCode =
                                await createSendEmailCodeWithDio(
                                  _regEmailCtrl.text,
                                  isLogin ? "login" : "register",
                                );
                            if (_sendEmailCode.code == 200) {
                              _tsk.XXTC("验证码发送成功", onlyOne: true);
                              _startCountDown(); // 开启倒计时
                            } else {
                              _tsk.XXTC(
                                _sendEmailCode.error ?? "",
                                onlyOne: true,
                              );
                            }
                          },
                    style: TextButton.styleFrom(
                      overlayColor: Color.fromARGB(255, 149, 198, 225),
                    ),
                    child: Text(
                      _codeBtnDisable ? "$_countDown s" : "获取验证码",
                      style: TextStyle(
                        color: _codeBtnDisable
                            ? Colors.grey
                            : Color.fromARGB(255, 149, 198, 225),
                        fontSize: 20,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 25),
          ],
        ),
      ),
    );
  }

  //登录校验
  bool _doLoginCheck() {
    final valid = _loginFormKey.currentState?.validate() ?? false;
    // if (!valid) return false;
    //  _tsk.XXTC("请输入邮箱或密码", onlyOne: true);
    String email = _loginEmailCtrl.text.trim();
    String pwd = _loginPwdCtrl.text.trim();
    if (email.isEmpty && pwd.isEmpty) {
      _tsk.XXTC("请输入邮箱或密码", onlyOne: true);
      return false;
    }
    if (!RegExp(r'^[\w.+-]+@[\w-]+\.[\w.-]+$').hasMatch(email)) {
      _tsk.XXTC("邮箱格式不正确", onlyOne: true);
      return false;
    }
    if (pwd.isEmpty) {
      _tsk.XXTC("请输入密码", onlyOne: true);
      return false;
    }
    return true;
  }

  //注册校验
  bool _doRegisterCheck() {
    final valid = _registerFormKey.currentState?.validate() ?? false;
    // if (!valid) return false;
    String email = _regEmailCtrl.text.trim();
    String pwd = _regPwdCtrl.text.trim();
    String confirmPwd = _regConfirmPwdCtrl.text.trim();
    String code = _regCodeCtrl.text.trim();
    if (email.isEmpty && pwd.isEmpty && confirmPwd.isEmpty && code.isEmpty) {
      _tsk.XXTC("输入注册信息", onlyOne: true);
      return false;
    }
    if (email.isEmpty) {
      _tsk.XXTC("请输入邮箱", onlyOne: true);
      return false;
    }
    if (!RegExp(r'^[\w.+-]+@[\w-]+\.[\w.-]+$').hasMatch(email)) {
      _tsk.XXTC("邮箱格式不正确", onlyOne: true);
      return false;
    }
    if (pwd.isEmpty) {
      _tsk.XXTC("请输入密码", onlyOne: true);
      return false;
    }
    if (confirmPwd.isEmpty) {
      _tsk.XXTC("请输入确认密码", onlyOne: true);
      return false;
    }
    if (pwd != confirmPwd) {
      _tsk.XXTC("两次输入密码不一致", onlyOne: true);
      return false;
    }
    if (code.isEmpty) {
      _tsk.XXTC("请输入验证码", onlyOne: true);
      return false;
    }
    return true;
  }

  Widget ZCDL() {
    return Column(
      children: [
        isLogin ? DLK() : ZCK(),
        ClassName.AJ(
          message: isLogin ? "登录" : "注册",
          onPressed: () async {
            bool ok;
            if (isLogin) {
              ok = _doLoginCheck();
              String md5Pwd = Md5().generateMd5(_loginPwdCtrl.text.toString());
              print(md5Pwd);
              var _reglogin = await createLoginWithDio(
                _loginEmailCtrl.text.toString(),
                md5Pwd,
              );
              if (ok) {
                print(_reglogin.code);
                // TODO 登录请求，可以在这里调用 JZTC loading
                if (_reglogin.code == 200) {
                  print(_reglogin.token);
                  Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(builder: (_) => SY()),
                    (route) => false,
                  );
                  print(
                    "登录 email=${_loginEmailCtrl.text}, pwd=${_loginPwdCtrl.text}",
                  );
                } else {
                  setState(() {
                    _tsk.XXTC(_reglogin.error ?? "", onlyOne: true, width: 260);
                  });
                }
              }
            } else {
              ok = _doRegisterCheck();
              if (ok) {
                // ========== 验证码校验接口 ==========
                var verifyRes = await createVerifyEmailCodeWithDio(
                  _regEmailCtrl.text.trim(),
                  _regCodeCtrl.text.trim(),
                  isLogin ? "login" : "register",
                );
                if (verifyRes.code == 200) {
                  // 验证码正确，执行注册
                  String newPwd = Md5().generateMd5(_regPwdCtrl.text.trim());
                  var registerRes = await createRegisterWithDio(
                    _regEmailCtrl.text.trim(),
                    newPwd,
                  );
                  if (registerRes.code == 200) {
                    print(registerRes.token);
                    _tsk.XXTC("注册成功", onlyOne: true);
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(builder: (_) => SY()),
                      (route) => false,
                    );
                  } else {
                    _tsk.XXTC(registerRes.error ?? "注册失败", onlyOne: true);
                  }
                } else {
                  // 验证码错误
                  print(verifyRes.code);
                  _tsk.XXTC(verifyRes.error ?? "验证码错误", onlyOne: true);
                }
              }
            }
          },
        ),
      ],
    );
  }

  @override
  void dispose() {
    //释放控制器
    _loginEmailCtrl.dispose();
    _loginPwdCtrl.dispose();
    _regEmailCtrl.dispose();
    _regPwdCtrl.dispose();
    _regConfirmPwdCtrl.dispose();
    _regCodeCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFE6F4FF),
      body: SafeArea(
        child: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              stops: [0.0, 1.0],
              colors: [Color.fromRGBO(234, 243, 255, 1), Color(0xFFFFFFFF)],
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              HYJM(),
              Expanded(
                child: SingleChildScrollView(child: Column(children: [ZCDL()])),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

final dio = Dio(
  BaseOptions(
    baseUrl: 'http://192.168.22.240:8000',
    connectTimeout: const Duration(seconds: 15),
    sendTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Accept': 'application/json'},
    responseType: ResponseType.json,
  ),
);

Future<Post> createLoginWithDio(String email, String pwd) async {
  final response = await dio.post<Map<String, dynamic>>(
    '/login',
    queryParameters: {'email': email, 'password': pwd},
  );
  final data = response.data;
  final status = response.statusCode;
  if (status == 200) {
    if (data == null) {
      throw const FormatException('创建接口没有返回文章');
    }
    return Post.fromJson(data);
  } else if (status == 400) {
    return Post.fromJson({
      'code': status,
      'error': '账号密码错误 / token失效',
      'token': null,
    });
  } else if (status == 404) {
    return Post.fromJson({'code': status, 'error': '接口地址不存在', 'token': null});
  } else if (status == 500) {
    return Post.fromJson({'code': status, 'error': '后端服务器异常', 'token': null});
  } else {
    return Post.fromJson({'code': status, 'error': '网络请求异常', 'token': null});
  }
}

Future<Post> createRegisterWithDio(String email, String pwd) async {
  String platform = getPlatformName();
  print("当前平台：$platform");
  if (platform == "web") {
    // web端单独逻辑
  } else if (platform == "android") {
    //安卓单独逻辑
  } else if (platform == "ios") {
    //苹果单独逻辑
  }
  final response = await dio.post<Map<String, dynamic>>(
    '/register',
    queryParameters: {'email': email, 'password': pwd, 'platform': platform},
  );
  final data = response.data;
  final status = response.statusCode;
  if (status == 200) {
    if (data == null) {
      throw const FormatException('创建接口没有返回文章');
    }
    return Post.fromJson(data);
  } else if (status == 400) {
    return Post.fromJson({
      'code': status,
      'error': '账号密码错误 / token失效',
      'token': null,
    });
  } else if (status == 404) {
    return Post.fromJson({'code': status, 'error': '接口地址不存在', 'token': null});
  } else if (status == 500) {
    return Post.fromJson({'code': status, 'error': '后端服务器异常', 'token': null});
  } else {
    return Post.fromJson({'code': status, 'error': '网络请求异常', 'token': null});
  }
}

Future<Post> createSendEmailCodeWithDio(String email, String scene) async {
  final response = await dio.get<Map<String, dynamic>>(
    '/send_email_code',
    queryParameters: {'email': email, 'scene': scene},
  );
  final data = response.data;
  final status = response.statusCode;
  if (status == 200) {
    if (data == null) {
      throw const FormatException('创建接口没有返回文章');
    }
    return Post.fromJson(data);
  } else if (status == 400) {
    return Post.fromJson({
      'code': status,
      'error': '账号密码错误 / token失效',
      'token': null,
    });
  } else if (status == 404) {
    return Post.fromJson({'code': status, 'error': '接口地址不存在', 'token': null});
  } else if (status == 500) {
    return Post.fromJson({'code': status, 'error': '后端服务器异常', 'token': null});
  } else {
    return Post.fromJson({'code': status, 'error': '网络请求异常', 'token': null});
  }
}

Future<Post> createVerifyEmailCodeWithDio(String email, String code,String scene) async {
  final response = await dio.post<Map<String, dynamic>>(
    '/verify_email_code',
    queryParameters: {'email': email, 'code': code,"scene":scene},
  );
  final data = response.data;
  final status = response.statusCode;
  if (status == 200) {
    if (data == null) {
      throw const FormatException('创建接口没有返回文章');
    }
    return Post.fromJson(data);
  } else if (status == 400) {
    return Post.fromJson({'code': status, 'error': '验证码错误', 'token': null});
  } else if (status == 404) {
    return Post.fromJson({'code': status, 'error': '接口地址不存在', 'token': null});
  } else if (status == 500) {
    return Post.fromJson({'code': status, 'error': '后端服务器异常', 'token': null});
  } else {
    return Post.fromJson({'code': status, 'error': '网络请求异常', 'token': null});
  }
}
