# StaticImagesToGIf
此工具可以将单张静态图片批量修改为拥有两帧相同图片的 GIF

程序小白，代码不足之处还请大佬多多指教
## 使用说明
1. 首次运行时会创建“img”、“GIF_path”文件夹
2. 将需要转换的静态图片存放至“img”文件夹中
3. 再次运行程序
4. 转换后的图片会存放至“GIF_path”文件夹中

## 注意事项
1. 程序包含的默认设置：图片的长或宽超过 1000 的，会自动转换为 999 并覆盖原图，转换时请务必注意备份保存
2. 目前无法保留含透明背景的图片，转换后透明背景会变为黑色

## 工具原理
- 读取文件夹内图片
- 检测图片分辨率是否超出限制
- 将图片复制一份至临时文件夹
- 将两个文件夹内的两张同名图片合并为 GIF

# 更新说明
## 2022-12-07
1. 新增对单帧 GIF、多帧 PNG 文件的判断与处理
2. 修复部分 BUG
3. 优化部分注释
