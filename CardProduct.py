import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from CardFactory import CardFactory
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.pagesizes import A4, A3, A2, A1, legal, landscape
from reportlab.lib.utils import ImageReader
import PIL.Image, PIL.ExifTags
from os import listdir
import os, re
import time
from reportlab.lib.units import inch


class CardProduct(QWidget):
    def __init__(self, name='MainForm'):
        super(CardProduct, self).__init__()
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('log2.ico'))
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.resize(500, 300)  # 设置窗体大小

        pIntvalidator = QIntValidator(self)
        pIntvalidator.setRange(1, 1000)

        fontSize = QLabel('设置字体大小:')
        self.fontSizeEdit = QLineEdit()
        self.fontSizeEdit.setValidator(pIntvalidator)
        self.fontSizeEdit.setText(str(120))

        qrCodeSize = QLabel('设置二维码大小:')
        self.qrCodeSizeEdit = QLineEdit()
        self.qrCodeSizeEdit.setValidator(pIntvalidator)
        self.qrCodeSizeEdit.setText(str(8))

        # 文件选择
        self.btn_backGround = QPushButton(self)
        self.btn_backGround.setObjectName("btn_backGround")
        self.btn_backGround.setText("选择背景图片")

        self.isCreQr = QCheckBox('生成二维码', self)
        self.isCreQr.toggle()

        # 文件选择
        self.btn_chooseFile = QPushButton(self)
        self.btn_chooseFile.setObjectName("btn_chooseFile")
        self.btn_chooseFile.setText("选择采集卡数据(仅支持.xlsx)")

        # 导出文件夹选择
        self.btn_chooseDir = QPushButton(self)
        self.btn_chooseDir.setObjectName("btn_chooseDir")
        self.btn_chooseDir.setText("选择图片导出文件夹")

        # 预览按钮
        self.btn_preview = QPushButton(self)
        self.btn_preview.setObjectName("btn_preview")
        self.btn_preview.setText("预览")

        # 提交按钮
        self.btn_submit = QPushButton(self)
        self.btn_submit.setObjectName("btn_submit")
        self.btn_submit.setText("开始执行")

        # 展示文本框
        self.textEdit = QTextEdit()
        self.file_choose = ''
        self.dir_choose = ''
        self.bgground = None
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_backGround)
        layout.addWidget(self.isCreQr)
        layout.addWidget(fontSize)
        layout.addWidget(self.fontSizeEdit)
        layout.addWidget(qrCodeSize)
        layout.addWidget(self.qrCodeSizeEdit)
        layout.addWidget(self.btn_chooseFile)
        layout.addWidget(self.btn_chooseDir)
        layout.addWidget(self.btn_preview)
        layout.addWidget(self.btn_submit)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.setWindowIcon(QIcon('favicon.ico'))
        # 设置信号
        self.btn_backGround.clicked.connect(self.slot_btn_chooseBg)
        self.btn_chooseDir.clicked.connect(self.slot_btn_chooseDir)
        self.btn_preview.clicked.connect(self.slot_btn_preview)
        self.btn_submit.clicked.connect(self.slot_btn_submit)
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.isCreQr.stateChanged.connect(self.changeFontSize)

    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                self.cwd,  # 起始路径
                                                                "All Files (*.xlsx)")
        self.file_choose = fileName_choose
        if fileName_choose == "":
            self.textEdit.setText("\n取消选择")
            return

        self.textEdit.setText("\n你选择的文件为:" + fileName_choose + ",\ntips: 数据量大的情况下程序会有卡顿，切勿关闭！！等待执行完毕")

    def slot_btn_chooseBg(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                self.cwd,  # 起始路径
                                                                "Images (*.png *.xpm *.jpg)")
        if fileName_choose == "":
            self.textEdit.setText("\n取消选择")
            return
        self.bgground = fileName_choose
        self.textEdit.setText("\n你选择的背景图片为:" + fileName_choose)

    def slot_btn_chooseDir(self):
        # 起始路径
        dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹", self.cwd)
        self.dir_choose = dir_choose
        if dir_choose == "":
            self.textEdit.setText("\n取消选择")
            return

        self.textEdit.setText("\n你选择的文件夹为:" + dir_choose)

    def run_task(self):
        # print(self.file_choose)
        self.textEdit.setText("\n正在生成，请耐心等待")
        card = CardFactory(self.dir_choose)
        data_frame = pd.read_excel(self.file_choose)
        data_values = data_frame.values
        i = len(data_values)
        if self.isCreQr.isChecked() is True:
            output_file_name = self.dir_choose + '/out.pdf'
        else:
            output_file_name = self.dir_choose + '/out-line.pdf'
        imgDoc = canvas.Canvas(output_file_name)  # pagesize=letter
        imgDoc.setFillColorRGB(0, 0, 1)
        imgDoc.setPageSize(A4)
        document_width, document_height = A4
        fontSize = 120
        qrcodeSize = 8
        if self.fontSizeEdit.text() != '':
            fontSize = int(self.fontSizeEdit.text())
        if self.qrCodeSizeEdit.text() != '':
            qrcodeSize = int(self.qrCodeSizeEdit.text())
        for data in data_values:
            if self.isCreQr.isChecked() is True:
                imgFile = card.product(data[0], self.bgground, fontSize, qrcodeSize, False)
            else:
                imgFile = card.productCode(data[0], self.bgground, fontSize, False)
            image_width, image_height = imgFile.size
            image_aspect = image_height / float(image_width)
            print_width = document_width
            print_height = document_width * image_aspect
            x = document_width - print_width
            y = document_height - print_height
            imgDoc.drawImage(ImageReader(imgFile), x,
                             y, width=print_width,
                             height=print_height, preserveAspectRatio=True)
            imgDoc.showPage()
        imgDoc.save()
        self.textEdit.setText("\n生成完毕！一共生成 " + str(i) + " 张卡片，卡片存放路径为，" + self.dir_choose)

    # 开始执行
    def slot_btn_submit(self):
        if self.file_choose == "":
            self.textEdit.setText("\n你选择的采集卡数据为空！！")
            return
        if self.dir_choose == "":
            self.textEdit.setText("\n你选择图片导出文件夹！！")
            return
        self.textEdit.setText(
            "\n正在执行。。。图片存放路径为：" + self.dir_choose)
        self.run_task()

    def slot_btn_preview(self):
        card = CardFactory()
        fontSize = 120
        qrcodeSize = 8
        if self.fontSizeEdit.text() != '':
            fontSize = int(self.fontSizeEdit.text())
        if self.qrCodeSizeEdit.text() != '':
            qrcodeSize = int(self.qrCodeSizeEdit.text())
        if self.isCreQr.isChecked() is True:
            card.product('2-EE000001', self.bgground, fontSize, qrcodeSize, True)
        else:
            card.productCode('2-EE000001', self.bgground, fontSize, True)

    def changeFontSize(self):
        if self.isCreQr.isChecked() is True:
            self.fontSizeEdit.setText(str(120))
        else:
            self.fontSizeEdit.setText(str(800))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = CardProduct('环保信息采集卡生成器(V2.0)')
    mainForm.show()
    sys.exit(app.exec_())
