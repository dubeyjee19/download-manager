from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
import humanize
from youtube_dl import *

ui,_ = loadUiType('main.ui')


class MainApp(QMainWindow , ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()

    def InitUI(self):
        # contain all ui changes in loading
        pass

    def Handle_Buttons(self):
        # handle all buttons in the app
        self.pushButton_9.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)

        self.pushButton_10.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        # calculate the progress
        read_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = read_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handle_Browse(self):
        # enable browsing to os , pick save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        print(save_location)

        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        # downloading any file
        print('Initializing Download')

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or Save Location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)
            except Exception:
                QMessageBox.warning(self, "Error", "Try Again")
                return
            QMessageBox.information(self, "Download Complete", "File downloaded successfully!")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    ################################################
    # Download YouTube Single Video
    def Save_Browse(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video_Data(self):
        video_url = self.lineEdit_3.text()
        print(video_url)

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams:
                print(humanize.naturalsize(stream.get_filesize()))
                size = humanize.naturalsize(stream.get_filesize())

                data = "{} {} {}".format(size, stream.quality, stream.extension)

                self.comboBox.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or Save Location")

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()

            download = video_stream[video_quality].download(filepath=save_location, callback=self.Video_Progress)
            QMessageBox.information(self, "Download Complete", "File downloaded successfully!")

        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.progressBar_2.setValue(0)

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = humanize.naturaltime(time)

            self.label_5.setText(str("{}".format(remaining_time)))
            QApplication.processEvents()

    ###########################################################
    # # # # # Youtube playlist download #######################
    def Playlist_Download(self):
        playlist_url = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or Save Location")



    def Playlist_Progress(self):
        pass

    ###########################################################

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
