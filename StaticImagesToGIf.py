import os
import shutil
from PIL import Image

# 初始化参数
path = os.getcwd()
# 原图片文件夹
img_path = os.path.join(path, "imgs")
# 图片拷贝文件夹
copy_of_img_path = os.path.join(path, "copy_of_imgs")
# GIF存放文件夹
GIF_path = os.path.join(path, "GIF_path")
# 图片列表（文件名）
img_files = []
# 复制后的图片列表
copy_imgs_list = []
# PNG 图片处理队列
PNG_list = []
# 指定尺寸
width = 999
height = 999


def main():
    """
    主程序
    :return: None
    """
    # 创建文件夹，用于存放图片
    print("文件根目录为：" + path)
    mkdir(img_path)
    mkdir(copy_of_img_path)
    mkdir(GIF_path)
    # 进行静态图片筛选
    img_files = filter_img(img_path)
    # 检查原图文件夹是否为空
    if (img_files != 0):
        print("图片转换中……")
        # 处理超出 1000*1000 分辨率的图片
        resize(img_files)
        # 复制图片文件
        copy_imgs_list = copy_imgs(img_path, copy_of_img_path, img_files)
        # 进行 GIF 转换
        img2gif(img_files, copy_imgs_list, GIF_path)
        print("GIF 转换成功，请进入“GIF_path”文件夹查看。")
        print("临时文件已删除！！")
        clear_temp()
    else:
        print('图片文件夹为空，请检查……')
        clear_temp()
        

# 过滤筛选非静态图片
def filter_img(path):
    """
    对图片进行筛选，修改异常图片（单帧 GIF 图，PNG 格式保存的 GIF 图等）
    :param path: 源图片文件路径
    :return: 图片文件名列表
    """
    # 获取原图文件夹内文件列表
    dir_files = os.listdir(path)
    # 文件列表不为空时继续执行，否则返回 0
    if (len(dir_files) != 0):
        print("文件列表：")
        print(dir_files)
        print("---------------------------------------")
        nfile = ""
        for file in dir_files:
            index = dir_files.index(file)
            # 分离文件名与后缀，进行筛选
            if os.path.splitext(file)[1] == ".png":
                # 将 .png 后缀修改为 gif，再进行帧数检查
                nfile = suffix_modification(file, 1)
                if check_fps(nfile) == 2:    # 帧数 > 1 代表原图应为 GIF 图片，保存后移动到 GIF 目录中
                    dir_files[index] = nfile
                    shutil.move(path + "\\" + dir_files[index],
                                GIF_path + "\\" + nfile)
                else:
                    # 帧数 <= 1 说明为单帧 PNG，后缀修改回 PNG
                    nfile = suffix_modification(nfile, 3)
                    dir_files[index] = nfile
                    img_files.append(dir_files[dir_files.index(file)])

            elif os.path.splitext(file)[1] == ".jpg" \
                    or os.path.splitext(file)[1] == ".jpeg":
                img_files.append(dir_files[dir_files.index(file)])

            # 遇到 GIF 文件自动移动到 GIF 文件夹中
            elif os.path.splitext(file)[1] == ".gif":
                nfile = file
                fps = check_fps(dir_files[index])
                if fps == 2:
                    shutil.move(path + "\\" + dir_files[dir_files.index(file)],
                            GIF_path + "\\" + dir_files[dir_files.index(file)])
                else:
                    # 帧数 <= 1 说明为单帧 GIF，后缀修改为 jpg
                    nfile = suffix_modification(nfile, 2)
                    dir_files[index] = nfile
                    img_files.append(dir_files[index])

        print("符合条件的文件为：")
        print(img_files)
        print("---------------------------------------")
        return img_files
    else:
        return 0


def suffix_modification(file, flag):
    """
    对以下情况通过 flag 判断，并修正后缀：
    1. 以 png 格式保存的多帧 gif；2. 以 png 格式保存的多帧 GIF 图；3. 还原 png 格式后缀
    :param file: 文件名.后缀
    :param flag: 1:改 .gif 后缀；2：改 .jpg 后缀；3：改 .png 后缀
    :return: 修改后的文件名.后缀
    """
    if flag == 1:
        shutil.move(os.path.join(img_path, file), os.path.join(img_path, os.path.splitext(file)[0] + ".gif"))
        file = os.path.splitext(file)[0] + ".gif"
        return file
    if flag == 2:
        shutil.move(os.path.join(img_path, file), os.path.join(img_path, os.path.splitext(file)[0] + ".jpg"))
        file = os.path.splitext(file)[0] + ".jpg"
        return file
    if flag == 3:
        shutil.move(os.path.join(img_path, file), os.path.join(img_path, os.path.splitext(file)[0] + ".png"))
        file = os.path.splitext(file)[0] + ".png"
        return file


def check_fps(img):
    """
    用于图片帧数检查
    :param img: 图片文件名
    :return: 0：异常及其他情况；1：单帧图片；2：多帧图片
    """
    print("对图片【{0}】进行帧数检查……".format(img))
    img = Image.open("imgs\\" + img)
    try:
        if img.n_frames > 1:
            return 2
        else:
            return 1
    except:
        return 0
    finally:
        print("帧数检查完成")


# 复制一份原图
def copy_imgs(path, copy_of_img_path, img_files):
    """
    :param path: 源文件文件夹路径
    :param copy_of_img_path: 源文件拷贝的文件夹路径
    :param img_files: 源文件的文件夹列表
    :return: 源文件拷贝的列表
    """
    for file_name in img_files:
        shutil.copy(path + "\\" + file_name, copy_of_img_path + "\\" + file_name)
    copy_imgs_list = os.listdir(copy_of_img_path)
    return copy_imgs_list


def mkdir(path):
    """
    检查并创建文件夹
    :param path: 所创建的文件夹名
    :return: None
    """
    if not os.path.exists(path):
        os.mkdir(path)


def clear_temp():
    """
    删除临时创建的文件夹
    :return: None
    """
    # 删除存放复制图片的文件夹
    if os.path.exists(copy_of_img_path):
        shutil.rmtree(copy_of_img_path)


def resize(img_files):
    """
    修改不符合微信表情包规则的图片，即长或宽 >= 1000 像素的图片
    :param img_files: 图片文件名列表
    :return: 0：出现异常；
    """
    if len(img_files) != 0:
        count = 0
        for i in range(len(img_files)):
            img = Image.open(os.path.join(img_path, img_files[i]))
            try:
                img_size = img.size  # [0]是宽，[1]是长
                # 查找超过 1000 * 1000 分辨率的图片
                if img_size[0] >= 1000 and img_size[1] >= 1000:
                    count += 1
                    # 修改分辨率
                    img_resize = img.resize((width, height), Image.Resampling.LANCZOS)
                    img_resize.save(img_path + "//" + img_files[i])
                elif img_size[0] >= 1000 and img_size[1] < 1000:
                    count += 1
                    # 修改分辨率
                    img_resize = img.resize((width, img_size[1]), Image.Resampling.LANCZOS)
                    img_resize.save(img_path + "//" + img_files[i])
                elif img_size[1] >= 1000 and img_size[0] < 1000:
                    count += 1
                    # 修改分辨率
                    img_resize = img.resize((img_size[0], height), Image.Resampling.LANCZOS)
                    img_resize.save(img_path + "//" + img_files[i])
            except:
                "发生异常！"
        if count != 0:
            print("检测出不符合分辨率标准的图片{0}张，正在处理中……".format(count))
        else:
            print("未发现超出分辨率图片，进入下一步处理。")
    else:
        return 0


def img2gif(img_files, copy_imgs_list, GIF_path):
    """
    完成 2 帧的 GIF 转换
    :param img_files: 图片的文件名列表
    :param copy_imgs_list: 复制图片的文件名列表
    :param GIF_path: 存放转换后 GIF 的路径
    :return:
    """
    for i in range(len(img_files)):
        gif_img = []
        gif_name = ""
        if img_files[i] == copy_imgs_list[i]:
            # GIF转换
            img = Image.open(os.path.join(img_path, img_files[i]))
            img = img.convert('RGBA').convert('P', palette=Image.Palette.ADAPTIVE)
            gif_img.append(img)
            img = Image.open(os.path.join(copy_of_img_path, copy_imgs_list[i]))
            img = img.convert('RGBA').convert('P', palette=Image.Palette.ADAPTIVE)
            gif_img.append(img)
            gif_name = img_files[i].split(".")[0] + ".gif"
        gif_img[0].save(GIF_path + "/" + gif_name, save_all=True, append_images=gif_img[1:],
                        transparency=254, duration=1, loop=0, disposal=2)


if __name__ == '__main__':
    main()
