# Smartinput-Upscaler
(中文 | [English](README_en.md))

起初是因为学校的祖传ppt太过于模糊，想尝试将其变清晰一些。
项目可以<b>Windows</b>以及<b>Linux</b>下运行。

项目基于[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)进行快速方便对各种图像/视频进行超分辨率处理。

项目使用了PyQt-Fluent-Widgets进行界面美化。

# TODO List

-   在图片放大之后进行(几乎)无损压缩
-   添加视频支持
-   图片批量处理

# 使用
目前支持图片与pdf输入，你可以在右边的<b>Releases</b>中下载对应系统版本，理论上应该开箱即用。以下为使用模型realesrgan-x4plus-anime处理图片的效果:

![pic](Pictures/Pic_compare.png)

注意，如果源pdf已经足够清晰，可能会起到反作用！(即更不清晰)

大部分情况下pdf转换效果如下：

![pdf](Pictures/PDF_compare.png)

## 多平台支持

![win](Pictures/Windows_start.png)
![Linux](Pictures/Linux_start.png)

## 模型与文件选择

由于后端采用的是[Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan)，能使用3种模型，并且支持Intel/AMD/Nvidia显卡加速。默认模型为适合通用图片处理的模型。

![model](Pictures/Model_choose.png)
![Select](Pictures/File_choose.png)

## 带剩余时间估计的进度条

![progress](Pictures/Progress_time.png)

# 从源码构建

## 安装python环境
    conda create -n pdf_up python=3.11
    conda activate pdf_up
    pip install PyMuPDF
    pip install pyqt6
    pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/
    python GUI.py
## 使用的模型来自项目 Real-ESRGAN ，请从下方下载可执行文件解压在根目录
[Real-ESRGAN_README](https://github.com/xinntao/Real-ESRGAN/blob/master/README_CN.md#%E4%BE%BF%E6%90%BA%E7%89%88%EF%BC%88%E7%BB%BF%E8%89%B2%E7%89%88%EF%BC%89%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6)
