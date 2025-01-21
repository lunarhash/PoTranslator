# PO文件批量翻译工具

这是一个使用Google翻译API批量翻译PO文件的Python脚本。本工具可以处理多达20,000行的大型PO文件。

## 功能特点

- 支持处理大型PO文件（最多20,000行）
- 实时显示翻译进度条
- 内置访问频率限制，避免触发API限制
- 错误处理机制，确保翻译过程不会中断
- 保留PO文件格式和元数据
- 支持自定义源语言和目标语言
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

### 基本用法
最简单的使用方式，将英文翻译为繁体中文：
```bash
python po_translate.py input.po
```

### 自定义语言
指定源语言和目标语言：
```bash
python po_translate.py input.po --from-lang en --to-lang zh-tw
```

### 支持的语言代码
常用的语言代码包括：
- 英语: en
- 简体中文: zh-CN
- 繁体中文: zh-TW
- 日语: ja
- 韩语: ko
- 更多语言代码请参考 [Google翻译支持的语言](https://cloud.google.com/translate/docs/languages)

## 参数说明

- `input_file`: 输入PO文件的路径
- `--from-lang`: 源语言代码（默认: en）
- `--to-lang`: 目标语言代码（默认: zh-tw）
- `--api-key`: Google Cloud Translation API密钥文件路径（可选）

## 示例

项目包含了一个示例PO文件，你可以用它来测试：
```bash
python po_translate.py example/example.po
```

## 输出文件

翻译后的文件将保存在输入文件的相同目录下，文件名会添加目标语言代码作为后缀。
例如: `messages.po` → `messages_zh-TW.po`

## 注意事项

1. 免费API可能有调用频率限制，脚本已内置了延迟机制
2. 建议先用小文件测试，确认效果后再处理大文件
3. 翻译完成后建议人工审核重要内容的翻译质量

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
