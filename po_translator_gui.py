import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QPushButton, 
                            QProgressBar, QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import polib
from deep_translator import GoogleTranslator
from datetime import datetime

LANGUAGES = {
    '简体中文': 'zh-CN',
    '繁体中文': 'zh-TW',
    '日语': 'ja',
    '韩语': 'ko',
    '英语': 'en',
    '法语': 'fr',
    '德语': 'de',
    '西班牙语': 'es',
    '俄语': 'ru'
}

class TranslatorThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, from_lang, to_lang):
        super().__init__()
        self.input_file = input_file
        self.from_lang = from_lang
        self.to_lang = to_lang

    def run(self):
        try:
            # 加载PO文件
            po = polib.pofile(self.input_file)
            total = len(po)
            self.status.emit(f"开始翻译，共找到 {total} 个字符串")
            
            # 初始化翻译器
            translator = GoogleTranslator(source=self.from_lang, target=self.to_lang)
            
            success_count = 0
            error_count = 0
            
            # 翻译每个条目
            for i, entry in enumerate(po):
                if entry.msgid and not entry.msgstr:
                    try:
                        translated = translator.translate(text=entry.msgid)
                        if translated:
                            entry.msgstr = translated
                            success_count += 1
                            self.status.emit(f"成功翻译: {entry.msgid} → {translated}")
                        else:
                            error_count += 1
                            self.status.emit(f"翻译失败: {entry.msgid}")
                    except Exception as e:
                        error_count += 1
                        self.status.emit(f"翻译错误 - {str(e)}: {entry.msgid}")
                
                # 更新进度
                progress = int((i + 1) / total * 100)
                self.progress.emit(progress)
            
            # 保存翻译后的文件
            output_file = self.input_file.rsplit('.', 1)[0] + f'_{self.to_lang}.po'
            po.save(output_file)
            
            # 发送完成信号
            self.finished.emit(f"翻译完成！\n成功：{success_count} 条\n失败：{error_count} 条\n保存至：{output_file}")
            
        except Exception as e:
            self.error.emit(f"发生错误：{str(e)}")

class DropArea(QWidget):
    fileDropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.label = QLabel("将PO文件拖放到这里\n或点击选择文件")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background-color: #f0f0f0;
            }
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toLocalFile().endswith('.po'):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.fileDropped.emit(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PO文件翻译工具')
        self.setMinimumSize(600, 400)

        # 主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 拖放区域
        self.drop_area = DropArea()
        self.drop_area.fileDropped.connect(self.handle_file)
        layout.addWidget(self.drop_area)

        # 文件选择按钮
        self.select_button = QPushButton('选择PO文件')
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # 语言选择区域
        lang_layout = QHBoxLayout()
        
        # 源语言选择
        from_lang_label = QLabel('源语言:')
        self.from_lang_combo = QComboBox()
        self.from_lang_combo.addItems(LANGUAGES.keys())
        self.from_lang_combo.setCurrentText('英语')
        lang_layout.addWidget(from_lang_label)
        lang_layout.addWidget(self.from_lang_combo)
        
        # 目标语言选择
        to_lang_label = QLabel('目标语言:')
        self.to_lang_combo = QComboBox()
        self.to_lang_combo.addItems(LANGUAGES.keys())
        self.to_lang_combo.setCurrentText('繁体中文')
        lang_layout.addWidget(to_lang_label)
        lang_layout.addWidget(self.to_lang_combo)
        
        layout.addLayout(lang_layout)

        # 开始翻译按钮
        self.translate_button = QPushButton('开始翻译')
        self.translate_button.clicked.connect(self.start_translation)
        self.translate_button.setEnabled(False)
        layout.addWidget(self.translate_button)

        # 进度条
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # 状态显示区域
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)

        self.current_file = None
        self.translator_thread = None

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择PO文件",
            "",
            "PO Files (*.po);;All Files (*)"
        )
        if file_name:
            self.handle_file(file_name)

    def handle_file(self, file_path):
        self.current_file = file_path
        self.drop_area.label.setText(f"已选择文件：{os.path.basename(file_path)}")
        self.translate_button.setEnabled(True)
        self.status_text.clear()
        self.progress_bar.setValue(0)

    def start_translation(self):
        if not self.current_file:
            return

        self.translate_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_text.clear()

        # 获取选择的语言代码
        from_lang = LANGUAGES[self.from_lang_combo.currentText()]
        to_lang = LANGUAGES[self.to_lang_combo.currentText()]

        # 创建并启动翻译线程
        self.translator_thread = TranslatorThread(self.current_file, from_lang, to_lang)
        self.translator_thread.progress.connect(self.update_progress)
        self.translator_thread.status.connect(self.update_status)
        self.translator_thread.finished.connect(self.translation_finished)
        self.translator_thread.error.connect(self.translation_error)
        self.translator_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_text.append(message)
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )

    def translation_finished(self, message):
        self.status_text.append("\n" + message)
        self.translate_button.setEnabled(True)

    def translation_error(self, message):
        self.status_text.append("\n错误：" + message)
        self.translate_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
