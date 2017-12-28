## Python识别验证码

只完成了图像的处理部分，其余识别功能尚未实现。可以用tesseract-ocr库来训练识别，不过这是另一个话题了。

### 环境

- python 3.6.3

### 运行

`python captcha.py`

### 结果说明

`/captchas`文件夹是放待处理的验证码

`/extracImags` 放的是将验证码某一颜色提取出来后的图片

`/cleanbgImgs` 放到是清除背景阈值处理后的图片

`/letters`放的是最终处理后字符图片，可以交给后续识别
