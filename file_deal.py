import fitz
import os
import tempfile
import subprocess
import platform
import shutil
import time

def deal(pdf_path,selected_option):
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    # 检查文件类型[TO DO]
    doc = fitz.open(pdf_path)
    # 遍历每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(temp_dir, f"page_{page_num + 1}.jpg")
        pix.save(image_path)

    # 关闭文档
    doc.close()
    # 检测操作系统
    os_name = platform.system()
    exe_path_windows = './realesrgan-ncnn-vulkan.exe'
    exe_path_linux = './realesrgan-ncnn-vulkan'
    exe_path = exe_path_windows if os_name == 'Windows' else exe_path_linux
    if os_name == 'Linux':
        subprocess.run(['chmod', 'u+x', exe_path_linux])
    model_name = selected_option
    # 构建命令行参数
    start_time = time.time()
    for i,imge_name in enumerate(os.listdir(temp_dir)):
        input_path = os.path.join(temp_dir, imge_name)
        cmd = [exe_path, '-i', input_path, '-o', input_path, '-n', model_name]
        subprocess.run(cmd)
        progress_percentage = int((i + 1) / len(os.listdir(temp_dir)) * 100)
        if progress_percentage >= 100:
            yield 99,start_time
        else:
            yield progress_percentage,start_time
    # 将图片转换为PDF
    doc = fitz.open()
    for imge_name in os.listdir(temp_dir):
        image_path = os.path.join(temp_dir, imge_name)
        img_doc = fitz.open(image_path)
        pdfbytes = img_doc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)
        img_doc.close()
    pdf_path = pdf_path.replace('.pdf', f'-{model_name}.pdf')
    doc.save(pdf_path)
    doc.close()
    # 删除临时目录
    shutil.rmtree(temp_dir)
    yield 100,start_time