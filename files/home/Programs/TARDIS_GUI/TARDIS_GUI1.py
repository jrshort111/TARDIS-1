#!/usr/bin/env python3
import sys, subprocess, os, urllib.request
from urllib.parse import urlparse
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QProgressBar, QPushButton
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QColor
from PyQt6.QtCore import Qt, QTimer

class TARDISGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TARDIS Music Dashboard")
        self.setGeometry(100, 100, 900, 500)

        # Theme
        self.apply_theme()

        # Main layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Left: ASCII TARDIS
        self.ascii_label = QLabel()
        self.ascii_label.setFont(QFont("Monospace", 8))
        self.ascii_label.setText(self.get_ascii())
        self.ascii_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.ascii_label)

        # Right: Track info + controls
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # Album art
        self.album_label = QLabel()
        self.album_label.setFixedSize(200,200)
        self.album_label.setStyleSheet("background-color: black;")
        self.right_layout.addWidget(self.album_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Song info
        self.song_label = QLabel("Loading song...")
        self.song_label.setFont(QFont("Monospace", 10))
        self.song_label.setWordWrap(True)
        self.right_layout.addWidget(self.song_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Progress
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.right_layout.addWidget(self.progress)

        # Time
        self.time_label = QLabel("00:00 / 00:00")
        self.right_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Controls
        self.controls_layout = QHBoxLayout()
        self.right_layout.addLayout(self.controls_layout)
        self.prev_btn = QPushButton("⏮️")
        self.play_btn = QPushButton("⏯️")
        self.next_btn = QPushButton("⏭️")
        for btn in [self.prev_btn, self.play_btn, self.next_btn]:
            self.controls_layout.addWidget(btn)
        self.prev_btn.clicked.connect(lambda: self.media_control("previous"))
        self.play_btn.clicked.connect(lambda: self.media_control("play-pause"))
        self.next_btn.clicked.connect(lambda: self.media_control("next"))

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_song)
        self.timer.start(1000)

        # Target player
        self.target_player = "chromium.instance7682"

        # Album cache
        self.album_cache = "/tmp/tardis_album.jpg"

    def apply_theme(self):
        palette = QApplication.palette()
        bg = palette.color(QPalette.ColorRole.Window).name()
        text = palette.color(QPalette.ColorRole.WindowText).name()
        accent = palette.color(QPalette.ColorRole.Highlight).name()
        self.setStyleSheet(f"background-color: {bg}; color: {text};")
        self.button_style = f"""
            QPushButton {{
                background-color: {accent};
                color: {text};
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {text};
                color: {accent};
            }}
        """

    def get_ascii(self):
        try:
            with open("/home/shorty/.config/neofetch/tardis.txt", "r") as f:
                return f.read()
        except:
            return "TARDIS ASCII not found"

    def media_control(self, command):
        subprocess.run(["playerctl", "--player", self.target_player, command])

    def update_song(self):
        try:
            title = subprocess.check_output(
                ["playerctl", "--player", self.target_player, "metadata", "title"],
                text=True
            ).strip()
            artist = subprocess.check_output(
                ["playerctl", "--player", self.target_player, "metadata", "artist"],
                text=True
            ).strip()
            self.song_label.setText(f"{title} - {artist}")

            # Album art
            art_url = subprocess.check_output(
                ["playerctl", "--player", self.target_player, "metadata", "mpris:artUrl"],
                text=True
            ).strip()
            if art_url:
                if not os.path.exists(self.album_cache) or art_url != getattr(self, "last_art_url", None):
                    self.last_art_url = art_url
                    parsed = urlparse(art_url)
                    if parsed.scheme == "file":
                        pixmap = QPixmap(parsed.path)
                    else:
                        urllib.request.urlretrieve(art_url, self.album_cache)
                        pixmap = QPixmap(self.album_cache)
                    self.album_label.setPixmap(pixmap.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio))

            # Progress
            length_micro = int(subprocess.check_output(
                ["playerctl", "--player", self.target_player, "metadata", "mpris:length"],
                text=True
            ).strip())
            position_micro = float(subprocess.check_output(
                ["playerctl", "--player", self.target_player, "position"],
                text=True
            ).strip())

            if length_micro > 0:
                self.progress.setValue(int((position_micro*1e6/length_micro)*100))

            # Track time
            pos_sec = int(position_micro)
            len_sec = int(length_micro/1_000_000)
            self.time_label.setText(f"{pos_sec//60:02d}:{pos_sec%60:02d} / {len_sec//60:02d}:{len_sec%60:02d}")

            # Apply button style (in case theme changes dynamically)
            for btn in [self.prev_btn, self.play_btn, self.next_btn]:
                btn.setStyleSheet(self.button_style)

        except subprocess.CalledProcessError:
            self.song_label.setText("No song playing")
            self.progress.setValue(0)
            self.time_label.setText("00:00 / 00:00")
            self.album_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TARDISGUI()
    gui.show()
    sys.exit(app.exec())
