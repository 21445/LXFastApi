import 'package:flutter/material.dart';
import 'package:flutterlx/DenLu/DL.dart';
import 'package:flutterlx/YingDaoYe/TP.dart';
import 'package:flutterlx/utils/storage.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';
import 'package:svg_flutter/svg_flutter.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  // 页面控制器
  final PageController controller = PageController();

  // 当前页索引
  int currentIndex = 0;
  
  /// 完成引导页
  // Future<void> finishGuide() async {
  //   // 获取本地缓存对象
  //   SharedPreferences prefs = await SharedPreferences.getInstance();

  //   // 保存已经看过引导页
  //   await prefs.setBool("guide", true);

  //   // 跳转登录页
  //   Navigator.pushReplacement(
  //     context,
  //     MaterialPageRoute(builder: (_) => home_page()),
  //   );
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // 渐变背景
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,

            colors: [Color.fromRGBO(234, 243, 255, 1), Color(0xFFFFFFFF)],
          ),
        ),

        child: SafeArea(
          child: Column(
            children: [
              /// =====================
              /// 顶部跳过按钮
              /// =====================
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 10,
                ),

                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,

                  children: [
                    TextButton(
                      // 点击跳过
                      onPressed: () {
                        // 完成引导页
                       

                        Storage.setNotFirstOpen();
                         print("完成引导，是否为第一次打开：${Storage.getIsFirstOpen()}");
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (_) => DL()),
                          
                        );
                      },

                      child: const Text(
                        "跳过",

                        style: TextStyle(color: Colors.grey, fontSize: 16),
                      ),
                    ),
                  ],
                ),
              ),

              /// =====================
              /// 页面区域
              /// =====================
              Expanded(
                child: PageView.builder(
                  // 页面控制器
                  controller: controller,
                  
                  // 页面数量
                  itemCount: onBoardList.length,

                  // 页面切换监听
                  onPageChanged: (index) {
                    setState(() {
                      // 更新当前页
                      currentIndex = index;
                    });
                  },

                  itemBuilder: (_, index) {
                    // 获取当前数据
                    final item = onBoardList[index];

                    return Padding(
                      padding: const EdgeInsets.all(30),

                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,

                        children: [
                          /// 3D插画
                          ///    仅在第4页显示
                          ///    其他页不显示
                          ///    图片高度为300
                          if (index != 3)
                            SvgPicture.asset(item.image, height: 300)
                          else
                            Image.asset(item.image, height: 200),
                          const SizedBox(height: 50),

                          /// 标题
                          Text(
                            item.title,

                            style: const TextStyle(
                              fontSize: 32,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF2F80ED),
                            ),
                          ),

                          const SizedBox(height: 20),

                          /// 描述
                          Text(
                            item.desc,

                            textAlign: TextAlign.center,

                            style: const TextStyle(
                              fontSize: 17,
                              color: Colors.grey,
                              height: 1.6,
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),

              /// =====================
              /// 底部区域
              /// =====================
              Padding(
                padding: const EdgeInsets.all(30),

                child: Column(
                  children: [
                    /// 小圆点动画
                    SmoothPageIndicator(
                      // 绑定控制器
                      controller: controller,

                      // 数量
                      count: onBoardList.length,

                      // 动画效果
                      effect: WormEffect(
                        dotHeight: 10,
                        dotWidth: 10,

                        activeDotColor: const Color(0xFF2F80ED),

                        dotColor: Colors.grey.shade300,
                      ),
                    ),

                    const SizedBox(height: 40),

                    /// 下一步按钮
                    SizedBox(
                      width: double.infinity,
                      height: 58,

                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF2F80ED),

                          elevation: 0,

                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(18),
                          ),
                        ),

                        onPressed: () {
                          // 最后一页
                          if (currentIndex == onBoardList.length - 1) {
                            // 完成引导
                            
                            Storage.setNotFirstOpen();
                            Navigator.pushReplacement(
                              context,
                              MaterialPageRoute(builder: (_) => DL()),
                            );
                          } else {
                            // 下一页动画
                            controller.nextPage(
                              duration: const Duration(milliseconds: 400),

                              curve: Curves.easeInOut,
                            );
                          }
                        },

                        child: Text(
                          currentIndex == onBoardList.length - 1
                              ? "立即开始"
                              : "下一步",

                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
