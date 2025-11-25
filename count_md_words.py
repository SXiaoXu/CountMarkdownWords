import os
import re

def clean_markdown(content):
    # 1. 去除代码块（```包裹的内容）
    content = re.sub(r'```[\s\S]*?```', '', content)
    # 2. 去除行内代码（`包裹的内容）
    content = re.sub(r'`[^`]+`', '', content)
    # 3. 处理链接：仅保留锚文本中的中文，删除英文和URL
    def extract_chinese_from_link(match):
        link_text = match.group(1)
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5]', link_text))
        return chinese_chars
    content = re.sub(r'\[(.*?)\]\([^)]*\)', extract_chinese_from_link, content)
    # 4. 处理图片：保留中文说明文本（![]内的中文），去除英文说明和URL
    def extract_chinese_from_image(match):
        img_desc = match.group(1)
        chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fa5]', img_desc))
        return chinese_chars
    content = re.sub(r'!\[(.*?)\]\([^)]*\)', extract_chinese_from_image, content)
    # 5. 去除Markdown格式符号
    content = re.sub(r'#+\s', '', content)
    content = re.sub(r'\*\*|\*|__|_', '', content)
    content = re.sub(r'---|___|\*\*\*', '', content)
    content = re.sub(r'>', '', content)
    content = re.sub(r'-|\*|\d+\.', '', content)
    content = re.sub(r'\\', '', content)
    content = re.sub(r'\|', '', content)
    content = re.sub(r'[:;"]', '', content)
    # 6. 去除时间戳
    content = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}', '', content)
    content = re.sub(r'\d{2}:\d{2}:\d{2}(?:\.\d+)?', '', content)
    content = re.sub(r'\d{4}年\d{2}月\d{2}日', '', content)
    # 7. 去除Hash值
    content = re.sub(r'[a-fA-F0-9]{32,64}', '', content)
    # 8. 去除多余空格、换行
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def count_valid_words(text):
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    return len(chinese_chars)

# 批量处理文件夹下所有.md文件（支持子文件夹递归扫描）
if __name__ == "__main__":
    # 工作目录：默认脚本所在文件夹
    md_folder = os.path.dirname(os.path.abspath(__file__))
    total_words = 0
    file_count = 0
    success_files = []  # 存储成功统计的文件信息（路径+字数）
    
    # 标题与分隔线（视觉优化）
    print("=" * 60)
    print("📋 Markdown文档有效字数统计工具（仅统计中文）")
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
    print("  1. 计入：链接锚文本中文、图片说明中文、普通中文内容")
    print("  2. 不计入：英文、URL、代码块、格式符号、时间戳、Hash值")
    print("=" * 60)