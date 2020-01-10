from PIL import Image, ImageDraw, ImageFont
import qrcode


class CardFactory:
    def __init__(self, saveFolder=None):
        self.saveFolder = saveFolder

    def product(self, codeText, bgGround=None, fontSize=120, qrcodeSize=8, preView=True):
        # qr对象
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=qrcodeSize, border=1)
        # 添加内容
        qr.add_data(codeText)
        qr.make(fit=True)
        qrImg = qr.make_image()
        qrImg = qrImg.convert("RGBA")
        # 背景图片
        background = "background.jpg"
        if bgGround is not None:
            background = bgGround
        backImg = Image.open(background)  # 这里是背景图片
        backImgW, backImgH = backImg.size
        qrImgW, qrImgH = qrImg.size
        w = int((backImgW - qrImgW) / 2)
        h = int((backImgH - qrImgH) / 2)
        backImg.paste(qrImg, (w, h), qrImg)
        draw = ImageDraw.Draw(backImg)
        ttfront = ImageFont.truetype('FZDHTJW.TTF', fontSize)  # 字体大小
        ttfrontSize = ttfront.getsize(codeText)
        fw = ttfrontSize[0]
        fh = ttfrontSize[1]
        fw = int((backImgW - fw) / 2)
        fh = int((backImgH - fh) / 2)
        draw.text((fw, h + qrImgH), codeText, fill=(0, 25, 25), font=ttfront)
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
    card.product('2-EE000002')
