import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
                              QFileDialog, QSlider, QSizePolicy, QGroupBox, QGridLayout, QListWidget,
                                QListWidgetItem, QDialog, QLabel, QProgressBar,QSplashScreen, QSpacerItem)

from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtMultimediaWidgets import QVideoWidget
from backnd import Video_summarizer

import time
import threading

print("Application started")


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Surveillance Summarizer")
        self.setGeometry(100, 100, 800, 600)

        # Create and show splash screen
        # splash_pix = QPixmap("logo_1.png")  # Replace "splash_image.png" with your splash image path
        # self.splash = SplashScreen(splash_pix)
        # self.splash.show()

        # Background
        central_widget = QWidget()
        background_layout = QVBoxLayout()
        background_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        

        # Next button
        next_button = QPushButton("Next", self)
        next_button.setStyleSheet("""
                                  *{
                                        background-color: #71797E;
                                        border-radius:10px;
                                        color: black;
                                        border: none;
                                  
                                        padding: 10px 75px;
                                        text-decoration: none;
                                        color: black;
                                        font-size: 25px;
                                        font-family: sans-serif;
                                        font-weight: 100;
                                  }*
                                  *:hover{
                                  background-color: #708090;
                                  }
                                  """)
        next_button.clicked.connect(self.showVideoUploadWindow)
        background_layout.addWidget(next_button)

        central_widget.setLayout(background_layout)
        self.setCentralWidget(central_widget)

    def showVideoUploadWindow(self):
        self.upload_window = VideoUploadWindow()
        self.setCentralWidget(self.upload_window)

class VideoUploadWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Video uploading button
        self.upload_button = QPushButton("Upload Video")
        self.upload_button.setStyleSheet("""
                                  *{
                                        background-color: #71797E;
                                        border-radius:10px;
                                        color: black;
                                        border: none;
                                  
                                        padding: 10px 75px;
                                        text-decoration: none;
                                        color: black;
                                        font-size: 25px;
                                        font-family: sans-serif;
                                        font-weight: 100;
                                        
                                  }*
                                  *:hover{
                                  background-color: #708090;
                                  }
                                  """)
        self.upload_button.clicked.connect(self.uploadVideo)
        self.layout.addWidget(self.upload_button)

        # Create a horizontal layout for the progress bar
        progress_layout = QHBoxLayout()
        self.layout.addLayout(progress_layout)

         # Create a progress bar to show progress
        self.progress_bar = QProgressBar(self)  # Create a QProgressBar widget
        self.layout.addWidget(self.progress_bar)  # Add the progress bar to the layout
        self.progress_bar.setVisible(False)  # Initially, progress bar is not visible
        
        

        self.Video_summarizer = None  # Initialize backnd's class instance to None



    def uploadVideo(self):
        self.file_dialog = QFileDialog()
        self.file_path, _ = self.file_dialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi)")
        if self.file_path:
            self.upload_button.setVisible(False)
            self.upload_button.setDisabled(True)

            # Reset progress bar to 0 and show it
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)

            self.loading_page(self.file_path)
            

    def loading_page(self,video_path):
        self.summarizer_obj = Video_summarizer(video_path=video_path)
        # Connect Worker's signal to update_progress_bar method
        self.summarizer_obj.update_progress.connect(self.update_progress_bar)
        # Connect Worker's finished signal to show_success_message method
        self.summarizer_obj.finished.connect(self.videoSummarized)
        # Start the worker thread
        self.summarizer_obj.start()

    def update_progress_bar(self, value):
        # Update the progress bar value
        self.progress_bar.setValue(value)

    def videoSummarized(self, total_videos):
        self.parent().setCentralWidget(VideoPlayerWindow(self.file_path, total_videos))


class VideoPlayerWindow(QWidget):
    def __init__(self, video_path, total_videos):
        super().__init__()
        
        self.video_path = video_path
        self.total_videos = total_videos

        # Video player
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile(video_path)) 
        self.media_player.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        print(video_path)

        # Video widget
        self.video_widget = QVideoWidget()

         # Video controls
        self.control_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.playVideo)
        self.pause_button = QPushButton("Pause")  # Fixed: Changed button text to "Pause"
        self.pause_button.clicked.connect(self.pauseVideo)  # Fixed: Changed clicked signal to pauseVideo
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopVideo)
        self.control_layout.addWidget(self.play_button)
        self.control_layout.addWidget(self.pause_button)  # Fixed: Added pause button
        self.control_layout.addWidget(self.stop_button)

        # Side window for summarized videos
        self.side_window = QGroupBox("Summarized Videos")
        self.side_layout = QVBoxLayout()
        self.summarized_videos_list = QListWidget()
        
        # total_videos = 5
        print(f"total : {total_videos}")
        for i in range(total_videos):
            video_tex = f"Output {i+1}"  # Changed to 1-indexed
            item = QListWidgetItem(video_tex)
            item.setData(Qt.ItemDataRole.UserRole, f"output/output{i+1}.mp4")  # Storing video file path
            self.summarized_videos_list.addItem(item)
        self.summarized_videos_list.itemClicked.connect(self.playSummarizedVideo)
        self.side_layout.addWidget(self.summarized_videos_list)
        self.side_window.setLayout(self.side_layout)
        

        # Main layout
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.video_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.side_window, 0, 1, 1, 1)
        self.main_layout.addLayout(self.control_layout, 1, 0, 1, 2)
        self.setLayout(self.main_layout)

        self.updateLayout()

        # Start video
        self.media_player.play()

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            # Set video output
            self.media_player.setVideoOutput(self.video_widget)


    def update_progress_bar(self, value):
        # Update the progress bar value
        self.progress_bar.setValue(value)

    def playVideo(self):
        self.media_player.play()

    def pauseVideo(self):  # Added method to pause the video
        self.media_player.pause()

    def stopVideo(self):
        self.media_player.stop()

    def playSummarizedVideo(self, item):
        video_path = item.data(Qt.ItemDataRole.UserRole)
        print(video_path[-5])
        if video_path:
            self.media_player.sourceChanged
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            print(item.data(Qt.ItemDataRole.UserRole))
            self.media_player.play()

    def updateLayout(self):
        # Set video widget to take larger portion and summarized video list to take smaller portion
        self.main_layout.setColumnStretch(0, 3)
        self.main_layout.setColumnStretch(1, 1)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
