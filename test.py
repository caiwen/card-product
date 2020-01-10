from PIL import Image, ImageDraw, ImageFont
import qrcode

qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=1)
codeText = "2-EE000001"
qr.add_data(codeText)
qr.make(fit=True)
qrImg = qr.make_image()
qrImg = qrImg.convert("RGBA")
backImg = Image.open("ppp.png")  # 这里是背景图片
backImg.paste(qrImg, (410, 200), qrImg)
draw = ImageDraw.Draw(backImg)
ttfront = ImageFont.truetype('FZDHTJW.TTF', 50)  # 字体大小
draw.text((425, 530), codeText, fill=(0, 25, 25), font=ttfront)
backImg.show()  # 显示图片,可以通过save保存
backImg.save(codeText + ".png")
