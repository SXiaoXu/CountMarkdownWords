import os
import re

def clean_markdown(content):
    # 1. 去除代码块（```包裹的内容）
    content = re.sub(r'```[\s\S]*?```', '', content)
    # 2. 去除行内代码（`包裹的内容）
    content = re.sub(r'`[^`]+`', '', content)
    # 3. 去除Markdown格式符号（标题、粗体、斜体、链接等）
    content = re.sub(r'#+\s', '', content)  # 去除标题#
    content = re.sub(r'\*\*|\*', '', content)  # 去除粗体/斜体*
    content = re.sub(r'\[|\]|\(|\)', '', content)  # 去除链接[]()
    content = re.sub(r'!\[.*?\]', '', content)  # 去除图片![]()
    content = re.sub(r'---|___', '', content)  # 去除分割线
    content = re.sub(r'>', '', content)  # 去除引用>
    content = re.sub(r'-|\*|\d+\.', '', content)  # 去除列表符号
    content = re.sub(r'\\', '', content)  # 去除转义符\
    # 4. 去除无意义字符（多余空格、换行、制表符）
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def count_valid_words(text):
    # 统计中文字符+英文单词（英文按空格分隔，中文直接计数）
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    english_words = re.findall(r'[a-zA-Z]+', text)
    return len(chinese_chars) + len(english_words)

# 批量处理文件夹下所有.md文件
if __name__ == "__main__":
    md_folder = os.getcwd()  # 当前文件夹（可改为具体路径，如 "C:/Docs/Markdown"）
    total_words = 0
    print("=== Markdown文档字数统计（去格式+去代码）===")
    for filename in os.listdir(md_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(md_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_content = clean_markdown(content)
            word_count = count_valid_words(cleaned_content)
            total_words += word_count
            print(f"{filename}: {word_count} 字")
    print(f"=== 总有效字数：{total_words} 字 ===")


    