import fitz
import os
import tempfile
import subprocess
import platform
import shutil
import time

def deal(file_path,selected_option):
    # 检查文件类型
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        yield from pdf(file_path,selected_option)
    elif file_type in ['png', 'jpg']:
        yield from image(file_path,selected_option)

def pdf(file_path,selected_option):
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    doc = fitz.open(file_path)
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
        if os_name == 'Windows':
            # 创建一个STARTUPINFO对象并设置隐藏属性
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(cmd, startupinfo=startupinfo)
            process.wait()
        else:
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
    file_path = file_path.replace('.pdf', f'-{model_name}.pdf')
    doc.save(file_path)
    doc.close()
    # 删除临时目录
    shutil.rmtree(temp_dir)
    yield 100,start_time


def image(file_path,selected_option):
    # 检测操作系统
    os_name = platform.system()
    exe_path_windows = './realesrgan-ncnn-vulkan.exe'
    exe_path_linux = './realesrgan-ncnn-vulkan'
    exe_path = exe_path_windows if os_name == 'Windows' else exe_path_linux
    if os_name == 'Linux':
        subprocess.run(['chmod', 'u+x', exe_path_linux])
    model_name = selected_option
    output_path = file_path.replace('.png', f'-{model_name}.png').replace('.jpg', f'-{model_name}.jpg')
    cmd = [exe_path, '-i', file_path, '-o', output_path, '-n', model_name]
    if os_name == 'Windows':
        # 创建一个STARTUPINFO对象并设置隐藏属性
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(cmd, startupinfo=startupinfo)
        process.wait()
    else:
        subprocess.run(cmd)
    yield 100,time.time()