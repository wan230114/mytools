#!/usr/bin/env python3

# 修复版PDF转PNG工具
# 使用最新的PyMuPDF库语法
# 安装方法: pip install PyMuPDF

"""
功能: 将PDF文件转换为PNG图片
用法: python pdf2png_modern.py your_pdf_file.pdf
"""

# 使用正确的导入方式，避免模块名冲突
import sys
import os

# 优先尝试直接导入PyMuPDF，如果失败则尝试其他方式
try:
    import fitz  # 现代版本的PyMuPDF直接使用fitz
    print("使用直接导入的fitz模块")
except ImportError:
    try:
        import pymupdf as fitz  # 部分环境可能需要这样导入
        print("使用pymupdf模块")
    except ImportError:
        print("错误: 未安装PyMuPDF库，请运行 'pip install PyMuPDF' 安装")
        sys.exit(1)

def pdf_to_images(pdf_path, zoom_x=5.0, zoom_y=5.0, rotation=0):
    """
    将PDF文件转换为PNG图像
    
    参数:
        pdf_path: PDF文件路径
        zoom_x: X方向缩放系数
        zoom_y: Y方向缩放系数
        rotation: 旋转角度
    
    返回:
        生成的图片文件列表
    """
    try:
        # 打开PDF文件
        doc = fitz.open(pdf_path)
        print(f"成功打开PDF文件: {pdf_path}")
        print(f"PDF页数: {len(doc)}")
        
        # 获取输出文件名前缀
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.dirname(pdf_path)
        if not output_dir:
            output_dir = '.'
        
        generated_files = []
        
        # 设置页码格式
        page_format = f"%0{len(str(len(doc)))}d" if len(doc) > 1 else ""
        
        # 遍历所有页面
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 设置转换矩阵
            matrix = fitz.Matrix(zoom_x, zoom_y)
            if rotation != 0:
                matrix = matrix.prerotate(rotation)
            
            # 获取页面的pixmap（现代版本使用get_pixmap而非getPixmap）
            try:
                # 现代PyMuPDF版本
                pix = page.get_pixmap(matrix=matrix, alpha=False)
            except AttributeError:
                # 兼容旧版本
                pix = page.getPixmap(matrix=matrix, alpha=False)
            
            # 生成输出文件名
            if page_format:
                page_str = page_format % (page_num + 1)
                output_path = os.path.join(output_dir, f"{base_name}{page_str}.png")
            else:
                output_path = os.path.join(output_dir, f"{base_name}.png")
            
            # 保存图像
            pix.save(output_path)
            generated_files.append(output_path)
            print(f"已保存页面 {page_num + 1}/{len(doc)} 到 {output_path}")
        
        # 关闭文档
        doc.close()
        print(f"转换完成，共生成 {len(generated_files)} 个图像文件")
        return generated_files
        
    except Exception as e:
        print(f"处理PDF文件时出错: {str(e)}")
        return []

def process_file(file_path):
    """处理单个文件"""
    if not os.path.isfile(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        return
    
    if not file_path.lower().endswith('.pdf'):
        print(f"警告: 跳过非PDF文件 - {file_path}")
        return
    
    print(f"\n处理文件: {file_path}")
    pdf_to_images(os.path.abspath(file_path))

def process_directory(dir_path):
    """处理目录中的所有PDF文件"""
    if not os.path.isdir(dir_path):
        print(f"错误: 目录不存在 - {dir_path}")
        return
    
    print(f"\n处理目录: {dir_path}")
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                process_file(file_path)

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法:")
        print("  python pdf2png_modern.py <pdf文件或目录>")
        print("\n示例:")
        print("  python pdf2png_modern.py document.pdf")
        print("  python pdf2png_modern.py pdf_folder/")
        return
    
    # 处理所有参数
    for path in sys.argv[1:]:
        abs_path = os.path.abspath(path)
        if os.path.isfile(abs_path):
            process_file(abs_path)
        elif os.path.isdir(abs_path):
            process_directory(abs_path)
        else:
            print(f"错误: 路径不存在 - {path}")

if __name__ == "__main__":
    print("=== PDF转PNG工具 (使用现代PyMuPDF库) ===")
    main()