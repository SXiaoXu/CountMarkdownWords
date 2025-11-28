import os
import re

def clean_markdown(content):
    # 1. 保留代码块和行内代码内容（参与计数）
    # 2. 处理链接：仅保留锚文本中的中文，删除英文和URL
    def extract_chinese_from_link(match):
        link_text = match.group(1)
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]', link_text))  # 包含中文标点
        return chinese_chars
    content = re.sub(r'\[(.*?)\]\([^)]*\)', extract_chinese_from_link, content)
    # 3. 处理图片：保留中文说明文本（![]内的中文+中文标点），去除英文说明和URL
    def extract_chinese_from_image(match):
        img_desc = match.group(1)
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]', img_desc))  # 包含中文标点
        return chinese_chars
    content = re.sub(r'!\[(.*?)\]\([^)]*\)', extract_chinese_from_image, content)
    # 4. 去除Markdown格式符号（不影响代码内容）
    content = re.sub(r'#+\s', '', content)  # 去除标题#
    content = re.sub(r'\*\*|\*|__|_', '', content)  # 去除粗体/斜体（*和_）
    content = re.sub(r'---|___|\*\*\*', '', content)  # 去除分割线
    content = re.sub(r'>', '', content)  # 去除引用>
    content = re.sub(r'\\', '', content)  # 去除转义符\
    content = re.sub(r'\|', '', content)  # 去除表格分隔符|
    # 5. 完全去除时间戳（含其中数字）
    content = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}', '', content)  # 日期格式（2024-10-01）
    content = re.sub(r'\d{2}:\d{2}:\d{2}(?:\.\d+)?', '', content)  # 时间格式（14:30:00）
    content = re.sub(r'\d{4}年\d{2}月\d{2}日', '', content)  # 中文日期格式（2024年10月1日）
    content = re.sub(r'\d{8,14}', '', content)  # 数字串时间戳（如20241001143000）
    # 6. 完全去除Hash值（含其中数字和字母）
    content = re.sub(r'[a-fA-F0-9]{32,64}', '', content)  # 32-64位Hash串（如a1b2c3d4...）
    # 7. 去除列表前的数字和符号（如"1." "2、"，避免误统计）
    content = re.sub(r'\d+[.)、]', '', content)
    # 8. 去除多余空格、换行（保留代码内容结构）
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def count_valid_words(text):
    # 统计规则：中文字符 + 中文标点 + 所有数字（除时间戳/Hash外）
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)  # 中文字符
    chinese_punctuation = re.findall(r'[\u3000-\u303f\uff00-\uffef]', text)  # 中文标点
    numbers = re.findall(r'\d', text)  # 所有非时间戳/Hash的数字
    return len(chinese_chars) + len(chinese_punctuation) + len(numbers)

# 批量处理文件夹下所有.md文件（支持子文件夹递归扫描）
if __name__ == "__main__":
    # 工作目录：默认脚本所在文件夹
    md_folder = os.path.dirname(os.path.abspath(__file__))
    total_words = 0
    file_count = 0
    success_files = []  # 存储成功统计的文件信息（路径+字数）
    
    # 标题与分隔线（视觉优化）
    print("=" * 60)
    print("📋 Markdown文档有效字数统计工具（含中文标点）")
    print(f"🔍 扫描目录：{md_folder}")
    print("=" * 60)
    print("【单个文件统计结果】")
    print("-" * 60)
    
    # 递归扫描所有.md文件
    for root, dirs, files in os.walk(md_folder):
        for filename in files:
            if filename.endswith(".md"):
                file_count += 1
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, md_folder)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    cleaned_content = clean_markdown(content)
                    word_count = count_valid_words(cleaned_content)
                    total_words += word_count
                    success_files.append((file_count, relative_path, word_count))
                    # 按序号输出，格式：序号 | 文件路径 | 字数
                    print(f"[{file_count:02d}] | {relative_path:<30} | {word_count:>6} 字")
                except Exception as e:
                    # 错误文件单独标记，不影响整体统计
                    print(f"[{file_count:02d}] | {relative_path:<30} | ❌ 读取失败：{str(e)}")
    
    # 统计汇总（突出总字数）
    print("-" * 60)
    print("【统计汇总】")
    print("-" * 60)
    print(f"📊 共扫描到 {file_count} 个Markdown文件")
    print(f"✅ 成功统计 {len(success_files)} 个文件")
    print(f"❌ 读取失败 {file_count - len(success_files)} 个文件")
    print(f"\n🎉 总有效字数：{total_words:,} 字")  # 千分位分隔，方便读取大数字
    print("=" * 60)
    print("📌 统计规则说明：")
    print("  1. 计入：中文字符、中文标点、正文中的数字、代码块/行内代码中的中文+标点+数字、链接/图片说明中的中文+标点")
    print("  2. 不计入：英文、URL、Markdown格式符号、时间戳（含数字）、Hash值（含数字）、列表前数字")
    print("=" * 60)