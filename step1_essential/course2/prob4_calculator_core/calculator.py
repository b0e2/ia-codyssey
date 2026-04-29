#
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QGridLayout, QPushButton, QLineEdit
)

class CalculatorConfig:
    WINDOW_TITLE = 'Calculator'
    WINDOW_SIZE = (300, 450)
    BG_COLOR = 'black'
    
    DISPLAY_STYLE = 'color: white; font-size: 50px; padding: 10px;'
    BTN_RADIUS = '30px'
    BTN_FONT = 'font-size: 20px; font-weight: bold;'
    
    # 버튼 타입별 색상 매핑: (배경색, 글자색)
    COLORS = {
        'op': ('#FF9F0A', 'white'),     # 연산자 
        'fn': ('#A5A5A5', 'black'),     # 상단 기능 
        'num': ('#333333', 'white'),    # 숫자 
    }
    
    # [수행과제] 출력 형태 및 버튼의 배치 데이터 구조화
    # 형식: (텍스트, 행, 열, 타입, [행스팬, 열스팬])
    BUTTONS = [
        ('AC', 0, 0, 'fn'), ('+/-', 0, 1, 'fn'), ('%', 0, 2, 'fn'), ('÷', 0, 3, 'op'),
        ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('x', 1, 3, 'op'),
        ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
        ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
        ('0', 4, 0, 'num', 1, 2), ('.', 4, 2, 'num'), ('=', 4, 3, 'op')
    ]
    

class Calculator:
    def __init__(self):
        pass


class CalculatorUI(QWidget):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())