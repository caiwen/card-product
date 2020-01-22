from PIL import Image, ImageDraw, ImageFont
import qrcode


class CardFactory:
    def __init__(self, saveFolder=None):
        self.saveFolder = saveFolder

    def productCode(self, codeText, bgGround=None, fontSize=800, preView=True, textW=0, textH=0):
        # 设置卡片的默认背景图片
        background = "background2.jpg"
        # 如果选择了默认背景图片，则取用选择的默认图片，如果没有选择则用默认的
        if bgGround is not None:
            background = bgGround
        #  打开卡片的默认背景图片
        backImg = Image.open(background)  # 这里是背景图片
        # 计算出图片的宽和高
        backImgW, backImgH = backImg.size
        # 加载字体
        ttfront = ImageFont.truetype('FZDHTJW2.TTF', fontSize)  # 字体大小
        # 获取到字体的吃错
        ttfrontSize = ttfront.getsize(codeText)
        # 构建画图
        draw = ImageDraw.Draw(backImg)
        # 字体的宽
        fw = ttfrontSize[0]
        # 字体的高
        fh = ttfrontSize[1]
        # 字体的横坐标
        fw = (backImgW - fw) / 2
        # 字体的纵坐标
        fh = (backImgH - fh) / 2
        # 将文字写入到画布中
        draw.text((fw + textW, fh + textH), codeText, fill=(255, 255, 255), font=ttfront)
        # 如果没有选择保存文件夹，则默认保存在根目录
        if self.saveFolder is None:
            savePath = codeText + "-line.png"
        else:
            savePath = self.saveFolder + "/" + codeText + "-line.png"
        # 选择预览，则显示图片，否在保存图片
        if preView is True:
            backImg.show()
            return None
        else:
            backImg.save(savePath)
            return backImg

    def product(self, codeText, bgGround=None, fontSize=120, qrcodeSize=8, preView=True, textW=0, textH=0):
        # qr对象
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=qrcodeSize, border=1)
        # 添加内容
        qr.add_data(codeText)
        qr.make(fit=True)
        # 二维码构建
        qrImg = qr.make_image()
        qrImg = qrImg.convert("RGBA")
        # 背景图片
        background = "background.jpg"
        # 如果选择了背景图片则用选择的背景图片
        if bgGround is not None:
            background = bgGround
        backImg = Image.open(background)  # 这里是背景图片
        # 背景图片的尺寸
        backImgW, backImgH = backImg.size
        # 二维码的尺寸
        qrImgW, qrImgH = qrImg.size
        # 二维码的坐标
        w = int((backImgW - qrImgW) / 2)
        h = int((backImgH - qrImgH) / 2)
        # 将二维码写在图片上
        backImg.paste(qrImg, (w, h), qrImg)
        draw = ImageDraw.Draw(backImg)
        ttfront = ImageFont.truetype('FZDHTJW.TTF', fontSize)  # 字体大小
        ttfrontSize = ttfront.getsize(codeText)
        fw = ttfrontSize[0]
        fh = ttfrontSize[1]
        fw = int((backImgW - fw) / 2)
        fh = int((backImgH - fh) / 2)
        draw.text((fw + textW, h + qrImgH + textH), codeText, fill=(0, 25, 25), font=ttfront)
        # backImg.show()  # 显示图片,可以通过save保存
        if self.saveFolder is None:
            savePath = codeText + ".png"
        else:
            savePath = self.saveFolder + "/" + codeText + ".png"
        if preView is True:
            backImg.show()
            return None
        else:
            backImg.save(savePath)
            return backImg


if __name__ == '__main__':
    # card = CardFactory('F:/采集卡')
    card = CardFactory()
    card.product('2-EE000002', textW=0, textH=20)
    # card.productCode('2-EE000002',textW=0,textH=-50)
