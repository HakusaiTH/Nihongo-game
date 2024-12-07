from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap, QBrush, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import random
import sys

questions = [
    {'question': '車', 'answers': ['รถยนต์', 'เรือ', 'เครื่องบิน', 'บ้าน'], 'correct_answer': 'รถยนต์'},
    {'question': '犬', 'answers': ['สุนัข', 'แมว', 'นก', 'ปลา'], 'correct_answer': 'สุนัข'},
    {'question': '猫', 'answers': ['สุนัข', 'แมว', 'เครื่องบิน', 'บ้าน'], 'correct_answer': 'แมว'},
    {'question': '山', 'answers': ['ภูเขา', 'แม่น้ำ', 'ทะเล', 'ป่า'], 'correct_answer': 'ภูเขา'},
    {'question': '川', 'answers': ['แม่น้ำ', 'ทะเล', 'แม่น้ำ', 'ทะเล'], 'correct_answer': 'แม่น้ำ'},
    {'question': '学校', 'answers': ['โรงเรียน', 'บ้าน', 'โรงพยาบาล', 'ร้านอาหาร'], 'correct_answer': 'โรงเรียน'},
    {'question': '魚', 'answers': ['ปลา', 'สุนัข', 'แมว', 'นก'], 'correct_answer': 'ปลา'},
    {'question': '花', 'answers': ['ดอกไม้', 'ต้นไม้', 'หิน', 'ไม้'], 'correct_answer': 'ดอกไม้'},
    {'question': '鳥', 'answers': ['นก', 'สุนัข', 'ปลา', 'แมว'], 'correct_answer': 'นก'},
    {'question': '空', 'answers': ['ท้องฟ้า', 'พื้นดิน', 'ภูเขา', 'ทะเล'], 'correct_answer': 'ท้องฟ้า'}
]

class LanguageLearningApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('สอนภาษาญี่ปุ่น')
        self.setGeometry(100, 100, 375, 588)

        self.set_background_image()
        self.play_background_music()

        self.layout = QVBoxLayout()

        self.lives_label = QLabel(f'ชีวิต: 5', self)
        self.lives_label.setAlignment(Qt.AlignLeft)
        self.lives_label.setFont(QFont('Arial', 16))
        self.lives_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.lives_label)

        self.current_question_number_label = QLabel(f'คำถามที่: 1', self)
        self.current_question_number_label.setAlignment(Qt.AlignLeft)
        self.current_question_number_label.setFont(QFont('Arial', 16))
        self.current_question_number_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.current_question_number_label)

        self.question_label = QLabel('คำถาม: ')
        self.question_label.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 24, QFont.Weight.Bold)
        self.question_label.setFont(font)
        self.question_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.question_label)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.lives = 5
        self.score = 0
        self.total_questions = len(questions)
        self.current_question_number = 1  
        self.next_question()

        self.setLayout(self.layout)

    def set_background_image(self):
        pixmap = QPixmap('D:/pyqt6/img/bg.jpg')
        if pixmap.isNull():
            print("Failed to load background image.")
            return

        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

    def play_background_music(self):
        self.player = QMediaPlayer()

        media_url = QUrl.fromLocalFile('D:/pyqt6/BGM.mp3')  
        self.media = QMediaContent(media_url)

        self.player.setMedia(self.media)
        self.player.setVolume(50)
        
        self.player.positionChanged.connect(self.loop_music)
        
        self.player.play()

    def loop_music(self, position):
        if position >= self.player.duration():
            self.player.setPosition(0)  
            self.player.play()  


    def next_question(self):
        if self.score == self.total_questions:
            self.show_congratulations()
            return

        if self.lives == 0:
            self.show_game_over_message()
            return

        self.current_question = random.choice(questions)
        question_text = self.current_question['question']
        correct_answer = self.current_question['correct_answer']
        answer_choices = self.current_question['answers']

        self.question_label.setText(f'คำถาม: {question_text}')
        self.create_answer_buttons(answer_choices)

        self.current_question_number_label.setText(f'คำถามที่: {self.current_question_number}')
        self.current_question_number += 1

    def create_answer_buttons(self, correct_answers):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        random.shuffle(correct_answers)
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for index, answer in enumerate(correct_answers):
            row, col = positions[index]
            button = QPushButton(answer, self)
            button.setFixedSize(180, 80)
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(self.check_answer)
            self.grid_layout.addWidget(button, row, col)

    def check_answer(self):
        clicked_button = self.sender()
        user_answer = clicked_button.text()
        correct_answer = self.current_question['correct_answer']

        if user_answer == correct_answer:
            self.score += 1
            self.show_message('ถูกต้อง!', 'คำตอบของคุณถูกต้อง!')
        else:
            self.lives -= 1
            if self.lives > 0:
                self.lives_label.setText(f'ชีวิต: {self.lives}')
                self.show_message('ผิดพลาด', f'คำตอบไม่ถูกต้อง! คุณเหลือชีวิต {self.lives} ชีวิต')
            else:
                self.show_game_over_message()

        self.next_question()

    def show_game_over_message(self):
        msg = QMessageBox()
        msg.setWindowTitle('หมดชีวิต!')
        msg.setText('คุณหมดชีวิตแล้ว! เริ่มต้นใหม่!')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.reset_game)
        msg.exec()

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec()

    def show_congratulations(self):
        msg = QMessageBox()
        msg.setWindowTitle('ยินดีด้วย!')
        msg.setText('คุณตอบครบทุกคำถามแล้ว! ยินดีด้วย!')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.reset_game)
        msg.exec()

    def reset_game(self, button):
        self.lives = 5
        self.score = 0
        self.lives_label.setText(f'ชีวิต: {self.lives}')
        self.current_question_number = 1  
        self.current_question_number_label.setText(f'คำถามที่: {self.current_question_number}')
        self.next_question()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LanguageLearningApp()
    window.show()
    sys.exit(app.exec())
