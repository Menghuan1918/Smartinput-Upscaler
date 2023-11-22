import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QProgressBar,
    QLabel,
    QFileDialog,
    QComboBox,
)
from PyQt6.QtCore import QTimer, Qt
import file_deal
import time
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject,QThreadPool

class WorkerSignals(QObject):
    progress = pyqtSignal(int, float)  # 进度百分比和开始时间

class Worker(QRunnable):
    def __init__(self, file_path, option):
        super(Worker, self).__init__()
        self.file_path = file_path
        self.option = option
        self.signals = WorkerSignals()

    def run(self):
        for progress_percentage, start_time in file_deal.deal(self.file_path, self.option):
            self.signals.progress.emit(progress_percentage, start_time)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        # 设置窗口标题
        self.setWindowTitle("Smartinput Upscaling")
        # 设置窗口大小
        self.resize(300, 150)
        # 设置窗口图标

        # 文件选择按钮
        self.fileButton = QPushButton("Select ☆ File(PDF/png/jpg)")
        self.fileButton.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.fileButton)

        # 选择按钮
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("realesr-animevideov3")
        self.comboBox.addItem("realesrgan-x4plus")
        self.comboBox.addItem("realesrgan-x4plus-anime")
        self.comboBox.setCurrentIndex(1)  # 设置默认选项为 realesrgan-x4plus
        self.layout.addWidget(self.comboBox)

        # 进度条
        self.progressBar = QProgressBar(self)
        self.layout.addWidget(self.progressBar)

        # 文字显示区域
        self.textLabel = QLabel("Time left:Unknown☆")
        self.layout.addWidget(self.textLabel)

        self.setLayout(self.layout)

    def openFileDialog(self):
        # 打开文件对话框并获取文件路径,支持pdf与图片
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ☆ File(PDF/png/jpg)", "", "PDF (*.pdf);;Images (*.png *.jpg)"
        )
        if file_path:
            self.fileButton.setEnabled(False)  # 禁用文件选择按钮
            self.startProcessing(file_path)

    def startProcessing(self, file_path):
        self.textLabel.setText('/ᐠ｡ꞈ｡ᐟ\Start Processing......')
        worker = Worker(file_path, self.comboBox.currentText())
        worker.signals.progress.connect(self.updateProgress)
        self.threadpool.start(worker)

    def updateProgress(self, progress, start_time):
        self.progressBar.setValue(progress)
        elapsed_time = time.time() - start_time
        if progress > 0:
            total_estimated_time = elapsed_time / (progress / 100)
            remaining_time = total_estimated_time - elapsed_time
            if remaining_time < 60:
                self.textLabel.setText(f'Time left: {remaining_time:.2f} S')
            else:
                self.textLabel.setText(f'Time left: {remaining_time // 60:.0f} M {remaining_time % 60:.2f} S')

        if progress >= 100:
            self.fileButton.setEnabled(True)
            self.textLabel.setText('Done☆(ᕑᗢᓫ∗)')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setWindowIcon = (QIcon("./icon.png"))
    ex.show()
    sys.exit(app.exec())
