# sizhu-programming

> **当老天是 Python 程序员**  
> 如果命运是一套预先封装好的程序，那么八字就是它的底层源代码。

用 Python 3.10+ 把传统四柱命理（八字）系统实现为**符号推理引擎**（Symbolic Reasoning Engine）。  
严格遵循邵伟华《四柱预测学》、沈孝瞻《子平真诠》及子平凡思博客理论，用枚举、数据类和查表逻辑实现，避免人工推盘错误。

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ 核心亮点

- 完整实现阴阳五行、天干地支、六十甲子、纳音等基础数据层
- 四柱排盘引擎（支持真太阳时、节气、时辰干支自动计算）
- 大运、流年计算
- 十神、格局、用神忌神、神煞、合冲刑害全模块
- 模块化设计，方便扩展成 Web / 命令行工具 / GUI

## 📖 完整文档

[**👉 点击阅读《四柱编程》完整教程**](sizhu_programming.md)

（第 0 章元认知 → 基础数据层 → 排盘引擎 → 分析模块 → 附录数据表）

📂 项目结构
textsizhu-programming/
├── README.md                 ← 你现在看到的首页
├── sizhu_programming.md      ← 完整技术文档（强烈推荐阅读）
├── sizhu/                    ← 即将上线的 Python 包（进行中）
│   ├── core/                 # 阴阳五行、天干地支等基础
│   ├── engine/               # 排盘引擎
│   └── analysis/             # 十神、格局、用神等
├── requirements.txt
└── LICENSE

🛠 技术栈

Python 3.10+
dataclasses + enum
lunar-python（农历转换）
可选：FastAPI / Streamlit（后续 Web 版本）

📬 参与贡献
欢迎 Issue、PR、讨论！
尤其是：

补充更多神煞 / 纳音数据
实现 Web 可视化界面
写测试用例

子平理论爱好者 & Python 工程师 共同维护。
