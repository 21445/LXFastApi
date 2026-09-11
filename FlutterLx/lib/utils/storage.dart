import 'package:shared_preferences/shared_preferences.dart';

/// 本地存储工具类
class Storage {
  // 是否已看过引导页的存储键
  static const String _guideKey = "guide";

  /// 是否为第一次打开（未看过引导页返回 true）
  static Future<bool> getIsFirstOpen() async {
    final prefs = await SharedPreferences.getInstance();
    return !(prefs.getBool(_guideKey) ?? false);//注释：判断是否为第一次打开，未看过引导页返回 true，已看过引导页返回 false
    
  }

  /// 标记引导页已看过
  static Future<void> setNotFirstOpen() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_guideKey, true);
  }
}
