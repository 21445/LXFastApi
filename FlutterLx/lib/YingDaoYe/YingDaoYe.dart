import 'package:flutter/material.dart';
import 'dart:async';

/// 主界面组件：App 启动页（闪屏页）
class KS extends StatefulWidget {
  KS({Key? key}) : super(key: key);

  @override
  _KSState createState() => _KSState();
}

/// KS 对应的状态类，负责构建页面 UI
class _KSState extends State<KS> with TickerProviderStateMixin {
  late AnimationController _shineController;
  late Animation<double> _shineAnimation;

  @override
  void initState() {
    super.initState();
    // 初始化流光动画
    _shineController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2600),
    )..repeat(); // 无限循环

    _shineAnimation = Tween<double>(begin: -0.3, end: 1.3).animate(
      CurvedAnimation(parent: _shineController, curve: Curves.easeInOut),
    );

    // ==========【在这里替换成你的真实题库加载逻辑】==========
    // 模拟加载，加载完成后跳转页面
    Timer(const Duration(seconds: 4), () {
      _shineController.stop();
      // Navigator.pushReplacement(context, MaterialPageRoute(builder: (ctx) => 你的首页()));
    });
  }

  @override
  void dispose() {
    // 释放动画资源，防止内存泄漏
    _shineController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // 占满整个屏幕
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          // 背景使用蓝到浅绿的线性渐变
          gradient: LinearGradient(
            // 渐变起点：顶部居中
            begin: Alignment.topCenter,
            // 渐变终点：底部居中
            end: Alignment.bottomCenter,
            // 还原图中蓝转浅绿渐变配色
            colors: [Color(0xFF90D0F0), Color(0xFFC8EED8)],
          ),
        ),
       child:  SafeArea(
    top: true,
    bottom: false, 
        child: Column(
          children: [
            // 顶部标题栏：左侧 App 名称，右侧版本号
            Container(
              padding: EdgeInsets.all(10),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                // 两端对齐，让标题和版本号分别靠左右
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '刷题宝',
                    style: TextStyle(
                      fontSize: 20,
                      color: const Color.fromARGB(206, 255, 255, 255),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'v1.0.0',
                    style: TextStyle(
                      fontSize: 20,
                      color: const Color.fromARGB(206, 255, 255, 255),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),

            // Expanded 让中间内容区占满剩余可用空间，实现垂直居中
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // 白色圆角图标容器（带底部投影效果）
                  Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(28),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black12,
                          blurRadius: 15,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    // 加载并显示 App 图标
                    child: Image.asset(
                      'lib/assets/images/app_icon.png',
                      width: 150,
                      height: 150,
                    ),
                  ),

                  const SizedBox(height: 24),
                  // App 名称大标题
                  const Text(
                    '刷题宝',
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 12),
                  // 副标题（宣传语）
                  const Text(
                    '科学高效 · 高效备考',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 24),
                  // 功能标签行：各标签在水平方向均匀分布
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: const [
                      FuncTag(text: '智能组卷', icon: Icons.flash_on),
                      FuncTag(text: '错题归纳', icon: Icons.info_outline),
                      FuncTag(
                        text: '成绩报告',
                        icon: Icons.emoji_events_outlined,
                      ),
                      // FuncTag(text: '学习记录', icon: Icons.history),
                      // FuncTag(text: '设置', icon: Icons.settings),
                    ],
                  ),
                ],
              ),
            ),

            // ========== 底部【带动画的进度条区域】==========
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: Column(
                children: [
                  // 进度条载体
                  SizedBox(
                    height: 5,
                    width: double.infinity,
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(6),
                      child: Stack(
                        children: [
                          // 底层底色
                          Container(
                            color: const Color.fromARGB(69, 255, 255, 255),
                          ),
                          // 滑动流光高光
                          AnimatedBuilder(
                            animation: _shineAnimation,
                            builder: (ctx, child) {
                              return Positioned(
                                left: MediaQuery.of(context).size.width * _shineAnimation.value * 0.75,
                                top: 0,
                                bottom: 0,
                                width: 70,
                                child: Container(
                                  decoration: BoxDecoration(
                                    color: Colors.white38,
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                ),
                              );
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Padding(
                    padding: EdgeInsets.only(bottom: 20),
                    child: Text(
                      "正在加载题库...",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.w400,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),)
    );
  }
}

/// 功能标签组件：显示一个带图标的圆角小标签
class FuncTag extends StatelessWidget {
  // 标签上显示的文字
  final String text;
  // 标签上显示的图标
  final IconData icon;

  // 构造函数：text 和 icon 为必填参数，必须在创建时传入
  const FuncTag({super.key, required this.text, required this.icon});

  // 重写 build 方法，构建组件的 UI
  @override
  Widget build(BuildContext context) {
    // 最外层容器：设置圆角背景与内边距
    return Container(
      // 水平 14、垂直 10 的内边距
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      // 背景装饰
      decoration: BoxDecoration(
        // 半透明白色背景
        color: const Color.fromARGB(61, 255, 255, 255),
        // 圆角半径为 16，使标签呈胶囊/圆角矩形样式
        borderRadius: BorderRadius.circular(16),
      ),
      // 容器内部：图标与文字水平排列
      child: Row(
        // 子组件列表
        children: [
          // 功能图标：白色半透明、大小为 18
          Icon(icon, color: Colors.white70, size: 18),
          // 图标与文字之间的水平间距
          const SizedBox(width: 4),
          // 功能文字：白色半透明、字号 16
          Text(
            text,
            style: const TextStyle(color: Colors.white70, fontSize: 16),
          ),
        ],
      ),
    );
  }
}
