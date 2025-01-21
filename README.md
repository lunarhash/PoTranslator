# PO文件批量翻译工具

这是一个使用Google翻译API批量翻译PO文件的Python脚本。本工具可以处理多达20,000行的大型PO文件，提供命令行和图形界面两种使用方式。

## 功能特点

- 支持处理大型PO文件（最多20,000行）
- 提供图形界面，支持拖放操作
- 支持多种常用语言互译
- 实时显示翻译进度
- 内置访问频率限制，避免触发API限制
- 错误处理机制，确保翻译过程不会中断
- 保留PO文件格式和元数据
- 支持免费翻译API，无需密钥

## 安装方法

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/po-translator.git
cd po-translator
```

2. 安装所需的Python包:
```bash
pip install -r requirements.txt
```

## 使用方法

### 图形界面版本（推荐）
运行图形界面程序：
```bash
python po_translator_gui.py
```

使用步骤：
1. 运行程序后会打开图形界面窗口
2. 将PO文件拖入虚线框内，或点击"选择PO文件"按钮
3. 在下拉菜单中选择源语言和目标语言
4. 点击"开始翻译"按钮
5. 等待翻译完成，可以在状态区域查看进度和结果

### 命令行版本
基本用法：
```bash
python po_translate.py input.po
```

自定义语言：
```bash
python po_translate.py input.po --from-lang en --to-lang zh-tw
```

## 支持的语言

常用的语言代码包括：
- 简体中文 (zh-CN)
- 繁体中文 (zh-TW)
- 日语 (ja)
- 韩语 (ko)
- 英语 (en)
- 法语 (fr)
- 德语 (de)
- 西班牙语 (es)
- 俄语 (ru)

更多语言支持请参考 [Google翻译支持的语言](https://cloud.google.com/translate/docs/languages)

## 参数说明

命令行版本参数：
- `input_file`: 输入PO文件的路径
- `--from-lang`: 源语言代码（默认: en）
- `--to-lang`: 目标语言代码（默认: zh-tw）

## 注意事项

1. 免费API可能有调用频率限制，脚本已内置了延迟机制
2. 建议先用小文件测试，确认效果后再处理大文件
3. 翻译完成后建议人工审核重要内容的翻译质量
4. 如果使用图形界面版本，确保已安装PyQt6

## 项目结构

```
po_translator/
├── README.md          # 项目说明文档
├── requirements.txt   # 项目依赖
├── po_translate.py    # 命令行版本主程序
├── po_translator_gui.py # 图形界面版本主程序
├── .gitignore        # Git忽略文件
├── LICENSE           # MIT许可证
└── example/          # 示例文件目录
    └── example.po    # 示例PO文件
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
