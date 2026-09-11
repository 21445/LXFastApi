import 'package:bot_toast/bot_toast.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutterlx/DenLu/SRK.dart';
import 'package:flutterlx/ShouYe/SYYD.dart';
import 'package:svg_flutter/svg.dart';

class DL extends StatefulWidget {
  DL({Key? key}) : super(key: key);

  @override
  _DLState createState() => _DLState();
}

class _DLState extends State<DL> {
  bool isLogin = false;

  // ========= 登录表单 =========
  final GlobalKey<FormState> _loginFormKey = GlobalKey<FormState>();
  final TextEditingController _loginPhoneCtrl = TextEditingController();
  final TextEditingController _loginPwdCtrl = TextEditingController();


  // ========= 注册表单 =========
  final GlobalKey<FormState> _registerFormKey = GlobalKey<FormState>();
  final TextEditingController _regPhoneCtrl = TextEditingController();
  final TextEditingController _regPwdCtrl = TextEditingController();
  final TextEditingController _regConfirmPwdCtrl = TextEditingController();
  final TextEditingController _regCodeCtrl = TextEditingController();

  final TSK _tsk = TSK();

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
                      _loginPhoneCtrl.clear();
                      _loginPwdCtrl.clear();
                      _regPhoneCtrl.clear();
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
                      _loginPhoneCtrl.clear();
                      _loginPwdCtrl.clear();
                      _regPhoneCtrl.clear();
                      _regPwdCtrl.clear();
                      _regConfirmPwdCtrl.clear();
                      _regCodeCtrl.clear();
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
            ClassName.TSC("手机号", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _loginPhoneCtrl,
                svgPath: "lib/assets/images/phone.svg",
                hintText: "请输入手机号",
                maxLength: 11,
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
  Widget ZCK() {
    return Container(
      padding: EdgeInsets.only(top: 20, left: 50, right: 50),
      child: Form(
        key: _registerFormKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClassName.TSC("手机号", FontWeight.w600),
            SizedBox(height: 8),
            Container(
              height: 50,
              child: ClassName.srk(
                controller: _regPhoneCtrl,
                svgPath: "lib/assets/images/phone.svg",
                hintText: "请输入手机号",
                maxLength: 11,
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
                      maxLength: 5,
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
                    onPressed: () {},
                    style: TextButton.styleFrom(
                      overlayColor: Color.fromARGB(255, 149, 198, 225),
                    ),
                    child: Text(
                      "获取验证码",
                      style: TextStyle(
                        color: Color.fromARGB(255, 149, 198, 225),
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
    //  _tsk.XXTC("请输入手机号或密码", onlyOne: true);

    String phone = _loginPhoneCtrl.text.trim();
    String pwd = _loginPwdCtrl.text.trim();

    if (phone.isEmpty && pwd.isEmpty) {
      _tsk.XXTC("请输入手机号或密码", onlyOne: true); 
      return false;
    }
    if (!RegExp(r'^1[3-9]\d{9}$').hasMatch(phone)) {
      _tsk.XXTC("手机号格式不正确", onlyOne: true);
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

    String phone = _regPhoneCtrl.text.trim();
    String pwd = _regPwdCtrl.text.trim();
    String confirmPwd = _regConfirmPwdCtrl.text.trim();
    String code = _regCodeCtrl.text.trim();

    if (phone.isEmpty && pwd.isEmpty && confirmPwd.isEmpty && code.isEmpty) {
      _tsk.XXTC("输入注册信息", onlyOne: true); 
      return false;
    }
    if (phone.isEmpty) {
      _tsk.XXTC("请输入手机号", onlyOne: true);
      return false;
    }
    if (!RegExp(r'^1[3-9]\d{9}$').hasMatch(phone)) {
      _tsk.XXTC("手机号格式不正确", onlyOne: true);
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
          onPressed: () {
            bool ok;
            if (isLogin) {
              ok = _doLoginCheck();
              if (ok) {
                //TODO 登录请求，可以在这里调用 JZTC loading
                if (_loginPhoneCtrl.text == "15678901234" &&
                    _loginPwdCtrl.text == "123456") {
                Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(builder: (_) => SY()),
                    (route) => false,
                  );
                  print(
                    "登录 phone=${_loginPhoneCtrl.text}, pwd=${_loginPwdCtrl.text}",
                  );
                }
              }
            } else {
              ok = _doRegisterCheck();
              if (ok) {
                //TODO 注册请求
                if (_regPhoneCtrl.text == "15678901234" &&
                    _regPwdCtrl.text == "123456" &&
                    _regConfirmPwdCtrl.text == "123456" &&
                    _regCodeCtrl.text == "1234") {
                  Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(builder: (_)=>SY()),
                    (route)=>false,
                  );
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
    _loginPhoneCtrl.dispose();
    _loginPwdCtrl.dispose();
    _regPhoneCtrl.dispose();
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
              colors: [
                Color.fromRGBO(234, 243, 255, 1),
                Color(0xFFFFFFFF),
              ],
            ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            HYJM(),
            Expanded(
              child: SingleChildScrollView(
                child: Column(children: [ZCDL()]),
              ),
            ),
          ],
        ),
      ),)
    );
  }
}