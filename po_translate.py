import polib
import time
import argparse
import os
from datetime import datetime
from tqdm import tqdm
from deep_translator import GoogleTranslator

LANGUAGE_MAPPING = {
    'zh-tw': 'zh-TW',
    'zh-cn': 'zh-CN',
    'en': 'en'
}

def normalize_lang_code(lang_code):
    """标准化语言代码"""
    return LANGUAGE_MAPPING.get(lang_code.lower(), lang_code)

def translate_po_file(input_file, from_lang='en', to_lang='zh-tw', api_key=None):
    """
    翻译PO文件从源语言到目标语言
    
    参数:
        input_file (str): 输入PO文件路径
        from_lang (str): 源语言代码
        to_lang (str): 目标语言代码
        api_key (str): Google Cloud Translation API密钥（可选）
    """
    # 标准化语言代码
    from_lang = normalize_lang_code(from_lang)
    to_lang = normalize_lang_code(to_lang)
    
    # 初始化翻译器
    if api_key:
        print("使用Google Cloud Translation API")
        # 如果提供了API密钥，使用官方Google Cloud Translation API
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
    else:
        print("使用免费翻译API")
    
    # 加载PO文件
    po = polib.pofile(input_file)
    total = len(po)
    print(f"\n开始翻译，共找到 {total} 个字符串需要翻译")
    print(f"源语言: {from_lang} -> 目标语言: {to_lang}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 使用tqdm创建进度条
    with tqdm(total=total, desc="翻译进度", ncols=100) as pbar:
        success_count = 0
        error_count = 0
        
        try:
            translator = GoogleTranslator(source=from_lang, target=to_lang)
        except Exception as e:
            print(f"初始化翻译器失败: {str(e)}")
            return
        
        for entry in po:
            if entry.msgid and not entry.msgstr:  # 只翻译msgstr为空的条目
                try:
                    # 翻译文本
                    translated = translator.translate(text=entry.msgid)
                    if translated:
                        entry.msgstr = translated
                        success_count += 1
                    else:
                        error_count += 1
                        print(f"\n翻译失败 - 原文: {entry.msgid}")
                    
                    # 更新进度条
                    pbar.update(1)
                    
                    # 休眠以避免触发API限制
                    time.sleep(0.5)
                    
                except Exception as e:
                    error_count += 1
                    print(f"\n翻译出错 - 原文: {entry.msgid}")
                    print(f"错误信息: {str(e)}")
                    continue
            else:
                pbar.update(1)
    
    # 保存翻译后的文件
    output_file = input_file.rsplit('.', 1)[0] + f'_{to_lang}.po'
    po.save(output_file)
    
    # 打印总结信息
    print(f"\n翻译完成！")
    print(f"成功翻译: {success_count} 条")
    print(f"失败条数: {error_count} 条")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"输出文件: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='PO文件翻译工具')
    parser.add_argument('input_file', help='输入PO文件路径')
    parser.add_argument('--from-lang', default='en', help='源语言代码 (默认: en)')
    parser.add_argument('--to-lang', default='zh-tw', help='目标语言代码 (默认: zh-tw)')
    parser.add_argument('--api-key', help='Google Cloud Translation API密钥文件路径（可选）')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"错误: 文件 {args.input_file} 不存在！")
        return
    
    translate_po_file(args.input_file, args.from_lang, args.to_lang, args.api_key)

if __name__ == '__main__':
    main()
