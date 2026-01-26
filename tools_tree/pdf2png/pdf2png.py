#!/home/chenjun/software/linux_tools/miniconda3/bin/python3.7

# 修复版PDF转PNG工具
# 使用最新的PyMuPDF库语法
# 安装方法:
# pip uninstall fitz
# pip install --upgrade pymupdf
# pip install PyMuPDF
# 修复版PDF转PNG工具 (兼容旧版PyMuPDF)
# 自动处理 'Pixmap' object has no attribute 'save' 错误

"""
功能: 将PDF文件转换为PNG图片
用法: python pdf2png_modern.py your_pdf_file.pdf
"""

import sys
import os

# 导入处理
try:
    import fitz 
except ImportError:
    try:
        import pymupdf as fitz
    except ImportError:
        print("错误: 未安装PyMuPDF库，请运行 'pip uninstall fitz; pip install PyMuPDF' 安装")
        sys.exit(1)

def pdf_to_images(pdf_path, zoom_x=5.0, zoom_y=5.0, rotation=0):
    try:
        doc = fitz.open(pdf_path)
        print(f"成功打开PDF文件: {pdf_path}")
        print(f"PDF页数: {len(doc)}")
        
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.dirname(pdf_path)
        if not output_dir: output_dir = '.'
        
        generated_files = []
        page_format = f"%0{len(str(len(doc)))}d" if len(doc) > 1 else ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 设置转换矩阵
            matrix = fitz.Matrix(zoom_x, zoom_y)
            if rotation != 0:
                matrix = matrix.prerotate(rotation)
            
            # 获取Pixmap (兼容写法)
            try:
                pix = page.get_pixmap(matrix=matrix, alpha=False)
            except AttributeError:
                pix = page.getPixmap(matrix=matrix, alpha=False)
            
            # 生成文件名
            if page_format:
                page_str = page_format % (page_num + 1)
                output_path = os.path.join(output_dir, f"{base_name}{page_str}.png")
            else:
                output_path = os.path.join(output_dir, f"{base_name}.png")
            
            # === 核心修复: 兼容保存方法 ===
            try:
                # 新版 PyMuPDF (v1.19.0+)
                pix.save(output_path)
            except AttributeError:
                # 旧版 PyMuPDF
                pix.writePNG(output_path)
            
            generated_files.append(output_path)
            print(f"已保存页面 {page_num + 1}/{len(doc)} 到 {output_path}")
        
        doc.close()
        print(f"转换完成，共生成 {len(generated_files)} 个图像文件")
        return generated_files
        
    except Exception as e:
        print(f"处理PDF文件时出错: {str(e)}")
        # 打印更详细的错误以便调试
        import traceback
        traceback.print_exc()
        return []

def process_file(file_path):
    if not os.path.isfile(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        return
    if not file_path.lower().endswith('.pdf'):
        print(f"警告: 跳过非PDF文件 - {file_path}")
        return
    print(f"\n处理文件: {file_path}")
    pdf_to_images(os.path.abspath(file_path))

def process_directory(dir_path):
    if not os.path.isdir(dir_path):
        print(f"错误: 目录不存在 - {dir_path}")
        return
    print(f"\n处理目录: {dir_path}")
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                process_file(os.path.join(root, file))

def main():
    if len(sys.argv) < 2:
        print("用法: python pdf2png.py <pdf文件或目录>")
        return
    for path in sys.argv[1:]:
        abs_path = os.path.abspath(path)
        if os.path.isfile(abs_path):
            process_file(abs_path)
        elif os.path.isdir(abs_path):
            process_directory(abs_path)
        else:
            print(f"错误: 路径不存在 - {path}")

if __name__ == "__main__":
    print("=== PDF转PNG工具 (兼容增强版) ===")
    main()