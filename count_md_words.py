import os
import re

def clean_markdown(content):
    # 1. 去除代码块（```包裹的内容）
    content = re.sub(r'```[\s\S]*?```', '', content)
    # 2. 去除行内代码（`包裹的内容）
    content = re.sub(r'`[^`]+`', '', content)
    # 3. 处理链接：仅保留锚文本中的中文，删除英文和URL（核心修改）
    # 匹配 [锚文本](URL) 格式，提取[]内的中文字符，删除其他内容
    def extract_chinese_from_link(match):
        link_text = match.group(1)
        # 仅保留锚文本中的中文字符，英文/数字/符号过滤
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5]', link_text))
        return chinese_chars
    content = re.sub(r'\[(.*?)\]\([^)]*\)', extract_chinese_from_link, content)
    # 4. 处理图片：保留中文说明文本（![]内的中文），去除英文说明和URL
    def extract_chinese_from_image(match):
        img_desc = match.group(1)
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5]', img_desc))
        return chinese_chars
    content = re.sub(r'!\[(.*?)\]\([^)]*\)', extract_chinese_from_image, content)
    # 5. 去除Markdown格式符号（标题、粗体、斜体、分割线等）
    content = re.sub(r'#+\s', '', content)  # 去除标题#
    content = re.sub(r'\*\*|\*|__|_', '', content)  # 去除粗体/斜体（*和_）
    content = re.sub(r'---|___|\*\*\*', '', content)  # 去除分割线
    content = re.sub(r'>', '', content)  # 去除引用>
    content = re.sub(r'-|\*|\d+\.', '', content)  # 去除列表符号（-、*、数字.）
    content = re.sub(r'\\', '', content)  # 去除转义符\
    content = re.sub(r'\|', '', content)  # 去除表格分隔符|
    content = re.sub(r'[:;"]', '', content)  # 去除无意义标点
    # 6. 去除时间戳（常见格式：YYYY-MM-DD、HH:MM:SS、YYYY/MM/DD等）
    content = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}', '', content)  # 日期格式
    content = re.sub(r'\d{2}:\d{2}:\d{2}(?:\.\d+)?', '', content)  # 时间格式
    content = re.sub(r'\d{4}年\d{2}月\d{2}日', '', content)  # 中文日期格式
    # 7. 去除Hash值（32位/40位/64位十六进制字符串）
    content = re.sub(r'[a-fA-F0-9]{32,64}', '', content)
    # 8. 去除多余空格、换行、制表符，合并为单个空格
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def count_valid_words(text):
    # 统计规则：仅统计中文字符（锚文本中文+图片中文说明+普通中文内容）
    # 匹配中文字符（不含中文标点，若需包含中文标点，可添加 \u3000-\u303f\uff00-\uffef）
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    return len(chinese_chars)

# 批量处理文件夹下所有.md文件（支持子文件夹递归扫描）
if __name__ == "__main__":
    # 工作目录：默认脚本所在文件夹（无需手动切换目录）
    md_folder = os.path.dirname(os.path.abspath(__file__))
    total_words = 0
    file_count = 0
    print("=== Markdown文档有效字数统计（最终优化版）===")
    print(f"扫描目录：{md_folder}")
    print("-" * 50)
    
    # 递归扫描所有.md文件（包括子文件夹）
    for root, dirs, files in os.walk(md_folder):
        for filename in files:
            if filename.endswith(".md"):
                file_count += 1
                file_path = os.path.join(root, filename)
                # 读取文件（强制UTF-8编码，避免中文乱码）
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # 清理内容+统计字数
                    cleaned_content = clean_markdown(content)
                    word_count = count_valid_words(cleaned_content)
                    total_words += word_count
                    # 输出相对路径（更清晰）
                    relative_path = os.path.relpath(file_path, md_folder)
                    print(f"✅ {relative_path}：{word_count} 字")
                except Exception as e:
                    print(f"❌ {filename}：读取失败（原因：{str(e)}）")
    
    print("-" * 50)
    print(f"📊 统计完成：共扫描 {file_count} 个Markdown文件")
    print(f"📝 总有效字数：{total_words} 字")
    # print("=== 统计规则说明 ===")
    # print("1. 计入：链接锚文本中的中文、图片说明中的中文、普通中文内容")
    # print("2. 不计入：英文（含锚文本英文）、URL、代码块、Markdown格式符号、时间戳、Hash值")


