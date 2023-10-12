import os
from converter import convert_heic_to_jpg
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, \
    QLineEdit, QTextEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, input_directory, output_directory):
        super().__init__()
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.stop_signal = False

    def run(self):
        heic_files = [f for f in os.listdir(self.input_directory) if f.lower().endswith(".heic")]

        if not heic_files:
            self.log_signal.emit('No HEIC files found in the input directory.')
            return

        for heic_file in heic_files:
            if self.stop_signal:
                self.log_signal.emit('Conversion stopped.')
                break

            input_path = os.path.join(self.input_directory, heic_file)
            output_path = os.path.join(self.output_directory, os.path.splitext(heic_file)[0] + ".jpg")

            if os.path.exists(output_path):
                self.log_signal.emit(f'Skipping {heic_file} as it already exists in the output directory.')
                continue

            if convert_heic_to_jpg(input_path, output_path):
                self.log_signal.emit(f'{heic_file} successfully converted')
            else:
                self.log_signal.emit(f'Error converting {heic_file}')

        self.log_signal.emit('Conversion process completed.')


class HEICtoJPGConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_text = QTextEdit(self)
        self.log_label = QLabel('Log:', self)
        self.stop_button = QPushButton('Stop', self)
        self.start_button = QPushButton('Start', self)
        self.center_frame = QFrame(self)
        self.output_browse_button = QPushButton('Browse', self.center_frame)
        self.output_entry = QLineEdit(self.center_frame)
        self.output_label = QLabel('Output Directory:', self.center_frame)
        self.input_browse_button = QPushButton('Browse', self.center_frame)
        self.input_entry = QLineEdit(self.center_frame)
        self.input_label = QLabel('Input Directory:', self.center_frame)
        self.worker_thread = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('HEIC to JPG Converter')

        self.center_frame.setGeometry(10, 50, 780, 100)
        self.center_frame.setFrameShape(QFrame.StyledPanel)
        self.center_frame.setFrameShadow(QFrame.Plain)

        input_layout = QHBoxLayout()
        input_layout2 = QHBoxLayout()

        center_layout = QVBoxLayout(self.center_frame)
        center_layout.addLayout(input_layout)
        center_layout.addLayout(input_layout2)

        self.input_label.setMinimumWidth(100)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_entry)
        input_layout.addWidget(self.input_browse_button)
        self.input_browse_button.clicked.connect(self.browse_input_directory)

        self.output_label.setMinimumWidth(100)
        input_layout2.addWidget(self.output_label)
        input_layout2.addWidget(self.output_entry)

        input_layout2.addWidget(self.output_browse_button)
        self.output_browse_button.clicked.connect(self.browse_output_directory)

        # START - STOP
        start_stop_frame = QFrame(self)
        start_stop_frame.setGeometry(0, 150, 800, 100)
        start_stop_layout = QHBoxLayout(start_stop_frame)

        self.start_button.clicked.connect(self.start_conversion)
        start_stop_layout.addWidget(self.start_button)

        self.stop_button.clicked.connect(self.stop_conversion)
        start_stop_layout.addWidget(self.stop_button)

        # LOG
        self.log_label.move(10, 220)

        self.log_text.setGeometry(10, 250, 780, 320)
        self.log_text.setReadOnly(True)

        self.setFixedSize(800, 600)

        self.show()

    def browse_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Input Directory')
        self.input_entry.setText(directory)

    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        self.output_entry.setText(directory)

    def start_conversion(self):
        input_directory = self.input_entry.text()
        output_directory = self.output_entry.text()

        if not input_directory or not output_directory:
            self.log_text.append('Error: Please select both input and output directories.')
            return

        self.worker_thread = WorkerThread(input_directory, output_directory)
        self.worker_thread.log_signal.connect(self.update_log)
        self.worker_thread.start()

    def stop_conversion(self):
        if self.worker_thread:
            self.worker_thread.stop_signal = True

    def update_log(self, text):
        self.log_text.append(text)

