import os
import shutil

from PIL import Image

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
# 指定尺寸
width = 999
height = 999


def main():
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
    # 获取原图文件夹内文件列表
    dir_files = os.listdir(path)
    # 文件列表不为空时继续执行，否则返回 0
    if (len(dir_files) != 0):
        print("文件列表：")
        print(dir_files)
        print("---------------------------------------")
        for file in dir_files:
            if os.path.splitext(file)[1] == ".png" \
                    or os.path.splitext(file)[1] == ".jpg" \
                    or os.path.splitext(file)[1] == ".jpeg":
                img_files.append(dir_files[dir_files.index(file)])
            # 遇到 GIF 文件自动移动到 GIF 文件夹中
            elif os.path.splitext(file)[1] == ".gif":
                shutil.move(path + "\\" + dir_files[dir_files.index(file)],
                            GIF_path + "\\" + dir_files[dir_files.index(file)])
        print("符合条件的文件为：")
        print(img_files)
        print("---------------------------------------")
        return img_files
    else:
        return 0


# 复制一份原图
def copy_imgs(path, copy_of_img, img_files):
    for file_name in img_files:
        shutil.copy(path + "\\" + file_name, copy_of_img + "\\" + file_name)
    copy_imgs_list = os.listdir(copy_of_img)
    return copy_imgs_list


# 创建文件夹
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


# 清除临时文件
def clear_temp():
    if os.path.exists(copy_of_img_path):
        shutil.rmtree(copy_of_img_path)

# 修改不符合表情包规则的图片
def resize(img_files):
    if len(img_files) != 0:
        count = 0
        for i in range(len(img_files)):
            img = Image.open(os.path.join(img_path, img_files[i]))
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
        if count != 0:
            print("检测出不符合分辨率标准的图片{0}张，正在处理中……".format(count))
        else:
            print("未发现超出分辨率图片，进入下一步处理。")
    else:
        return 0


# 转换 GIF
def img2gif(img_files, copy_imgs_list, GIF_path):
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
