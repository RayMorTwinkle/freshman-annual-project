#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕JSON转Markdown工具
将JSON格式的字幕文件转换为只包含content的Markdown格式
"""

import json
import os
import glob
from pathlib import Path

def should_skip_conversion(json_filename, output_dir):
    """
    检查是否应该跳过转换
    
    Args:
        json_filename (str): JSON文件名（不含扩展名）
        output_dir (str): 输出目录
        
    Returns:
        bool: True表示应该跳过，False表示应该转换
    """
    # 检查输出目录是否存在
    if not os.path.exists(output_dir):
        return False
    
    # 检查是否存在完全同名的文件
    same_name_file = os.path.join(output_dir, f"{json_filename}.md")
    if os.path.exists(same_name_file):
        return True
    
    # 检查是否存在以json_filename开头的文件（如10：学习.md）
    for filename in os.listdir(output_dir):
        if filename.startswith(json_filename) and filename.endswith('.md'):
            return True
    
    return False

def convert_json_to_md(json_file_path, output_dir="markdown_output"):
    """
    将单个JSON字幕文件转换为Markdown格式
    
    Args:
        json_file_path (str): JSON文件路径
        output_dir (str): 输出目录
    """
    try:
        # 获取JSON文件名（不含扩展名）
        json_filename = Path(json_file_path).stem
        
        # 检查是否应该跳过转换
        if should_skip_conversion(json_filename, output_dir):
            print(f"⏭ 跳过: {json_file_path} (已存在同名或相关文件)")
            return
        
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 确保数据是列表格式
        if not isinstance(data, list):
            print(f"警告: {json_file_path} 的数据格式不是列表，跳过处理")
            return
        
        # 提取所有content内容
        contents = []
        for item in data:
            if isinstance(item, dict) and 'content' in item:
                content = item['content'].strip()
                if content:  # 只添加非空内容
                    contents.append(content)
        
        if not contents:
            print(f"警告: {json_file_path} 中没有找到有效的内容，跳过处理")
            return
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{json_filename}.md")
        
        # 写入Markdown文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {json_filename}\n\n")
            f.write("## 字幕内容\n\n")
            
            for i, content in enumerate(contents, 1):
                f.write(f"{i}. {content}\n\n")
        
        print(f"✓ 已转换: {json_file_path} -> {output_file}")
        print(f"  共提取 {len(contents)} 条字幕内容")
        
    except json.JSONDecodeError as e:
        print(f"错误: {json_file_path} 不是有效的JSON文件: {e}")
    except Exception as e:
        print(f"错误: 处理 {json_file_path} 时发生错误: {e}")

def batch_convert_json_files(directory=".", output_dir="markdown_output"):
    """
    批量转换目录中的所有JSON文件
    
    Args:
        directory (str): 包含JSON文件的目录
        output_dir (str): 输出目录
    """
    # 查找所有JSON文件
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    if not json_files:
        print(f"在目录 {directory} 中没有找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件:")
    for file in json_files:
        print(f"  - {os.path.basename(file)}")
    
    print(f"\n开始转换...")
    
    # 转换每个JSON文件
    success_count = 0
    skip_count = 0
    for json_file in json_files:
        # 获取JSON文件名（不含扩展名）
        json_filename = Path(json_file).stem
        
        # 检查是否应该跳过转换
        if should_skip_conversion(json_filename, output_dir):
            print(f"⏭ 跳过: {json_file} (已存在同名或相关文件)")
            skip_count += 1
            continue
            
        try:
            convert_json_to_md(json_file, output_dir)
            success_count += 1
        except Exception as e:
            print(f"✗ 转换失败: {json_file} - {e}")
    
    print(f"\n转换完成! 成功转换 {success_count} 个文件，跳过 {skip_count} 个文件")
    print(f"输出文件保存在: {os.path.abspath(output_dir)}")

def main():
    """主函数"""
    print("=" * 60)
    print("字幕JSON转Markdown工具")
    print("=" * 60)
    
    # 设置当前工作目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    print(f"工作目录: {current_dir}")
    
    # 批量转换
    batch_convert_json_files(".", "markdown_output")
    
    print("\n使用说明:")
    print("- 所有转换后的Markdown文件保存在 'markdown_output' 目录中")
    print("- 每个文件包含原始JSON中的所有 'content' 字段")
    print("- 内容按顺序编号，方便阅读")
    print("- 如果输出目录中已存在同名或相关文件（如10：学习.md），将跳过转换")

if __name__ == "__main__":
    main()