import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

# 앱 전체에서 사용되는 상수와 데이터 구조
class Config:
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

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        # [수행과제] 아이폰 계산기와 최대한 유사하게 계산기 UI를 만든다.
        self.expression = ''
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(Config.WINDOW_TITLE)
        # 튜플 언패킹을 활용한 인자 전달
        self.setFixedSize(*Config.WINDOW_SIZE)
        self.setStyleSheet(f'background-color: {Config.BG_COLOR};')

        layout = QVBoxLayout(self)
        
        # 디스플레이 설정
        self.label = QLabel('0')
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.label.setStyleSheet(Config.DISPLAY_STYLE)
        layout.addWidget(self.label)

        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Config에 분리해둔 데이터를 불러와 버튼 생성
        for btn_data in Config.BUTTONS:
            self._add_button(grid, btn_data)

        layout.addLayout(grid)

    def _add_button(self, grid, data):
        text, row, col, b_type = data[:4]
        span = data[4:]
        
        button = QPushButton(text)
        button.setFixedSize(130 if text == '0' else 60, 60)
        button.setStyleSheet(self._get_style(b_type))
        
        # [수행과제] 각각의 버튼을 누를 때 마다 숫자가 입력 될 수 있게 이벤트를 처리한다.
        button.clicked.connect(lambda ch, t=text: self.on_click(t))
        grid.addWidget(button, row, col, *span)

    def _get_style(self, b_type):
        """Config에서 색상을 가져와 스타일 문자열 완성"""
        bg, fg = Config.COLORS.get(b_type)
        return f'background-color: {bg}; color: {fg}; border-radius: {Config.BTN_RADIUS}; {Config.BTN_FONT}'

    def on_click(self, char):
        # [보너스과제] 4칙 연산이 가능하도록 코드를 추가한다.
        
        actions = {
            'AC': self._clear,
            '=': self._calculate,
            '+/-': self._toggle_sign
        }
        
        if char in actions:
            actions[char]()
        else:
            self._append_char(char)

        self.label.setText(self.expression or '0')

    def _clear(self):
        self.expression = ''

    def _calculate(self):
        try:
            # 화면의 'x'와 '÷'를 파이썬이 계산할 수 있는 '*'와 '/'로 치환
            calc_expr = self.expression.replace('x', '*').replace('÷', '/')
            result = eval(calc_expr)
            self.expression = str(int(result) if result == int(result) else result)
        except Exception:
            self.expression = 'Error'

    def _toggle_sign(self):
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression

    def _append_char(self, char):
        self.expression = char if self.expression == '0' else self.expression + char


# [수행과제] Python으로 UI를 만들 수 있는 PyQt 라이브러리를 설치한다.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec())