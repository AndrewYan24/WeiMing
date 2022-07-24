import os
import fitz
import tkinter as tk
from PyPDF2 import PdfFileReader
from tkinter import filedialog

'''
pdf_path：PDF存储位置，靠交互获得
png_output：转换后图片输出目录，靠交互获得
'''
root = tk.Tk()
root.withdraw()

pdf_path = filedialog.askopenfilename()  # 用户选择需要转换的PDF文件


def get_filename(file_path):  # 获取文件名模块
    """获取不带路径和后缀的文件名
    :param file_path: PDF路径
    """
    _, fullname = os.path.split(file_path)
    filename, _ = os.path.splitext(fullname)
    return filename


def get_filepage(file_path):
    """
    :param file_path: PDF路径
    :return:
    """
    reader = PdfFileReader(file_path)
    if reader.isEncrypted:
        reader.decrypt('')
    page_name = reader.getNumPages()
    return page_name


def pdf_image(pdf_file, img_path, zoom_x=4, zoom_y=4, rotation_angle=0):  # 转换PDF并输出为以页码命名的图片模块
    """将PDF文件转成PNG图片
    :param pdf_file: PDF文件路径
    :param img_path: 保存图片的路径
    :param zoom_x: 缩放比例（横向）
    :param zoom_y: 缩放比例（纵向）
    :param rotation_angle: 旋转角度
    """
    pdf = fitz.open(pdf_file)
    for page_num in range(get_filepage(pdf_path)):
        page_obj = pdf[page_num]
        # 创建用于图像变换的矩阵
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        # 将PDF页面处理成图像
        pm = page_obj.get_pixmap(matrix=trans, alpha=False)
        temp = get_filename(pdf_file)
        pm.save(f'{img_path}{page_num + 1}.png')
    pdf.close()


png_output_path = ('require/' + str(get_filename(pdf_path)) + '/')  # 主程序模块
print('正在创建目录')
while_num = 0
while os.path.exists(str(png_output_path)) is True:
    while_num = while_num + 1
    png_output_path = ('require/' + str(get_filename(pdf_path)) + '_' + str(while_num) + '/')
else:
    os.makedirs(str(png_output_path))
print('目录创建完毕')
rel_output_path = png_output_path
print('即将开始转换图片…')
pdf_image(pdf_path, png_output_path, 10, 10, 0)
print('转换图片完成')  # 图片转换标志
transform = 1
pdf_page = (get_filepage(pdf_path))