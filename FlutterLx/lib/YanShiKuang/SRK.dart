import 'package:bot_toast/bot_toast.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:svg_flutter/svg.dart';

class ClassName {
  // 输入框
  static Widget srk({
    required String svgPath,
    required String hintText,
    int maxLength = 5,
    required String? Function(String?) validator,
    bool obscureText = false,
    TextEditingController? controller,
  }) {
    return TextFormField(
      style: const TextStyle(fontSize: 20, color: Color.fromARGB(205, 8, 8, 8)),
      maxLines: 1,
      controller: controller,
      inputFormatters: [LengthLimitingTextInputFormatter(maxLength)],
      obscureText: obscureText,
      decoration: InputDecoration(
        hintText: hintText,
        contentPadding: const EdgeInsets.symmetric(vertical: 25),
        errorStyle: const TextStyle(height: 0, fontSize: 0),
        hintStyle: const TextStyle(color: Colors.grey, fontSize: 14),
        filled: true,
        fillColor: const Color(0xffedf4f8),
        prefixIcon: Padding(
          padding: const EdgeInsets.all(15),
          child: SvgPicture.asset(
            svgPath,
            colorFilter: const ColorFilter.mode(Colors.grey, BlendMode.srcIn),
          ),
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide.none,
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: Colors.red),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: Colors.red, width: 1),
        ),
      ),
      validator: validator,
    );
  }

  //按钮：把点击事件onPressed交给外面
  static Widget AJ({required String message, required VoidCallback onPressed}) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 50),
      height: 50,
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 149, 198, 225),
        borderRadius: BorderRadius.circular(10),
      ),
      child: TextButton(
        onPressed: onPressed,
        child: Center(
          child: Text(
            message,
            style: const TextStyle(color: Colors.white, fontSize: 20),
          ),
        ),
      ),
    );
  }

  static Widget TSC(String message, FontWeight? fontWeight) {
    return Text(
      message,
      style: TextStyle(
        fontSize: 15,
        color: Color.fromARGB(183, 0, 0, 0),
        fontWeight: fontWeight,
      ),
    );
  }
}

class TSK {
  /// 自定义Toast提示弹窗【BotToast封装】
  /// [message] 要显示的提示文本，必填
  /// [fontWeight] 文字字重，可选；不传使用默认
  /// [align] toast弹出位置，可选；默认 [Alignment.center]
  /// [color] 文字颜色，可选；不传使用默认
  /// [bgColor] 背景颜色，可选；不传使用默认
  /// [borderRadius] 圆角半径，可选；默认 [10]
  /// [height] 弹窗高度，可选；默认 [60px]
  /// [width] 弹窗宽度，可选；默认 [200px]
  /// [onlyOne] 是否只显示一个弹窗，可选；默认 [true]
  void XXTC(
    String message, {
    FontWeight? fontWeight,
    Alignment? align,
    Color? color,
    Color? bgColor,
    double? borderRadius,
    double? height,
    double? width,
    bool? onlyOne,
  }) {
    BotToast.showCustomText(
      align: align ?? Alignment.center,
      onlyOne: onlyOne ?? true,
      toastBuilder: (cancel) {
        return Container(
          height: height ?? 60,
          width: width ?? 200,
          // padding: EdgeInsets.only(left: 30,right: 30),
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: bgColor ?? const Color.fromARGB(182, 100, 100, 100),
            borderRadius: BorderRadius.circular(borderRadius ?? 10),
          ),
          child: Text(
            message,
            style: TextStyle(
              fontSize: 20,
              color: color ?? const Color.fromARGB(183, 255, 255, 255),
              fontWeight: fontWeight,
            ),
          ),
        );
      },
    );
  }

  /// 自定义Toast提示弹窗【BotToast封装】
  /// [message] 要显示的提示文本，必填
  /// [duration] 弹窗显示时间，可选；默认 [2秒]
  /// [color] 文字颜色，可选；不传使用默认
  /// [bgColor] 背景颜色，可选；不传使用默认
  /// [height] 弹窗高度，可选；默认 [60px]
  /// [width] 弹窗宽度，可选；默认 [100px]
  /// [heightjiaz] 加载图标高度，可选；默认 [30px]
  /// [widthjiaz] 加载图标宽度，可选；默认 [30px]
  /// [strokeWidth] 加载图标宽度，可选；默认 [2px]

  CancelFunc JZTC(
    String message, {
    int? duration,
    Color? color,
    Color? bgColor,
    double? height,
    double? width,
    double? heightjiaz,
    double? widthjiaz,
    double? strokeWidth,
  }) {
    return BotToast.showCustomLoading(
      duration: Duration(seconds: duration ?? 2),

      toastBuilder: (cancel) {
        return Container(
          height: height ?? 100,
          width: width ?? 100,
          decoration: BoxDecoration(
            color: bgColor ?? const Color.fromARGB(182, 100, 100, 100),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                height: heightjiaz ?? 30,
                width: widthjiaz ?? 30,
                child: CircularProgressIndicator(
                  color: color ?? Colors.white,
                  valueColor: AlwaysStoppedAnimation(Colors.white),
                  strokeWidth: strokeWidth ?? 2,
                ),
              ),
              SizedBox(height: 8),
              Text(
                message,
                style: TextStyle(
                  fontSize: 10,
                  color: color ?? Colors.white,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

/// context：上下文
/// message：弹窗显示文字
/// delaySeconds：延迟多少秒自动关闭
void showAutoCloseDialog(
  BuildContext context, {
  required String message,
  int delaySeconds = 2,
}) {
  showDialog(
    context: context,
    barrierDismissible: true,
    builder: (BuildContext dialogContext) {
      Future.delayed(Duration(seconds: delaySeconds), () {
        if (Navigator.canPop(dialogContext)) {
          Navigator.pop(dialogContext);
        }
      });

      return AlertDialog(
        backgroundColor: Colors.transparent,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16), // 大圆角美化
        ),
        content: Text(message),
        actions: [
          // TextButton(
          //   onPressed: () {
          //     Navigator.pop(dialogContext);
          //   },
          //   child: const Text("确定"),
          // ),
        ],
      );
    },
  );
}


