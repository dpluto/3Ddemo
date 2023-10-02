import os
import PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path



from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox

def handleCalc():
    info = textEdit1.toPlainText()

    # 薪资20000 以上 和 以下 的人员名单
    salary_above_20k = ''
    salary_below_20k = ''
    for line in info.splitlines():
        if not line.strip():
            continue
        parts = line.split(' ')
        # 去掉列表中的空字符串内容
        parts = [p for p in parts if p]
        name,salary,age = parts
        if int(salary) >= 20000:
            salary_above_20k += name + '\n'
        else:
            salary_below_20k += name + '\n'

    QMessageBox.about(window,
                '统计结果',
                f'''薪资20000 以上的有：\n{salary_above_20k}
                \n薪资20000 以下的有：\n{salary_below_20k}'''
                )

app = QApplication([])

window = QMainWindow()
window.resize(1600, 1000)
window.move(300, 310)
window.setWindowTitle('图像识别')

textEdit1 = QPlainTextEdit(window)
textEdit1.setPlaceholderText("图像显示")
textEdit1.move(10,25)
textEdit1.resize(1000,950)

textEdit2 = QPlainTextEdit(window)
textEdit2.setPlaceholderText("目标ID： ZA001  数量： 3   ")
textEdit2.move(1050,25)
textEdit2.resize(500,600)

textEdit3 = QPlainTextEdit(window)
textEdit3.setPlaceholderText("识别程序状态输出")
textEdit3.move(1060,560)
textEdit3.resize(475,55)

button = QPushButton('开始', window)
button.move(1100,800)
button.resize(200,100)


button.clicked.connect(handleCalc)

window.show()

app.exec_()