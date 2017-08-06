from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib.request


class CuteDownloader(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()
        self.url_edit = QLineEdit()
        self.file_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")
        browse = QPushButton("Browse Location")

        self.url_edit.setPlaceholderText("URL here")
        self.file_location.setPlaceholderText("File Location")
        self.progress.setValue(0)

        layout.addWidget(self.url_edit)
        layout.addWidget(self.file_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)
        self.setWindowTitle("Cute Downloader")
        self.setMinimumSize(500, 300)
        self.setFocus()

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse)

    def browse(self):
        save_location = QFileDialog.getSaveFileName(self,"Save File As", ".")
        self.file_location.setText(QDir.toNativeSeparators(save_location))

    def download(self):
        url = self.url_edit.text()
        file = self.file_location.text()

        try:
            urllib.request.urlretrieve(url, file, reporthook=self.report)
        except Exception:
            QMessageBox.warning(self, "Warning", "Download failed")
            return

        QMessageBox.information(self, "Information", "Download Complete")
        self.progress.setValue(0)
        self.url_edit.setText("")
        self.file_location.setText("")

    def report(self, blocksize, blocknum, totalsize):
        d = blocknum*blocksize
        if totalsize > 0:
            percent = d*100/totalsize
            self.progress.setValue(int(percent))


app = QApplication(sys.argv)
dialog = CuteDownloader()
dialog.show()
sys.exit(app.exec_())