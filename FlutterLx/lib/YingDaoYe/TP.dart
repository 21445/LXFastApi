// 引导页数据模型
class OnBoardModel {

  // 图片路径
  final String image;

  // 标题
  final String title;

  // 描述
  final String desc;

  // 构造函数
  OnBoardModel({
    required this.image,
    required this.title,
    required this.desc,
  });
}

// 引导页数据列表
List<OnBoardModel> onBoardList = [

  // 第1页
  OnBoardModel(
    image: "lib/assets/images/YDY10.svg",
    title: "海量题库",
    desc: "精选优质题库，随时随地开始刷题",
  ),

  // 第2页
  OnBoardModel(
    image: "lib/assets/images/YDY7.svg",
    title: "智能分析",
    desc: "AI自动分析你的薄弱知识点",
  ),

  // 第3页
  OnBoardModel(
    image: "lib/assets/images/YDY9.svg",
    title: "学习报告",
    desc: "实时查看学习数据与成长轨迹",
  ),
  // 第4页
  OnBoardModel(
    image: "lib/assets/images/app_icon.png",
    title: "刷题宝",
    desc: "开启你的刷题之旅，提升你的解题能力",
  ),
];