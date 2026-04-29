from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Config:
    WINDOW_SIZE = (390, 760)
    BG_COLOR = 'black'
    BTN_SIZE = 78
    BTN_GAP = 10
    COLORS = {
        'op': ('#F99A2E', 'white'),
        'fn': ('#666666', 'white'),
        'num': ('#303030', 'white'),
    }
    DISPLAY = 'color:white;font-size:{size}px;font-weight:300;'
    EXPRESSION = 'color:#8E8E93;font-size:28px;font-weight:300;'
    BUTTON = (
        'background:{bg};color:{fg};border:none;border-radius:39px;'
        'font-size:34px;font-weight:300;'
    )
    # [수행과제] 버튼 배치 데이터를 구조화한다.
    BUTTONS = [
        ('⌫', 'AC', '%', '÷'),
        ('7', '8', '9', 'x'),
        ('4', '5', '6', '-'),
        ('1', '2', '3', '+'),
        ('+/-', '0', '.', '='),
    ]


class Calculator:
    def __init__(self) -> None:
        self.reset()

    # [수행과제] 계산기 상태를 초기화한다.
    def reset(self) -> dict:
        self.current = '0'
        self.expression = ''
        self.left = None
        self.operator = None
        self.new_input = False
        self.done = False
        return self._state()

    # [수행과제] 숫자와 소수점 입력을 처리한다.
    def input_number(self, number: str) -> dict:
        if self.current == 'Error' or self.done:
            self.reset()
        if self.new_input or self.current == '0':
            self.current = number
            self.new_input = False
        else:
            self.current += number
        self._refresh_expression()
        return self._state()

    def input_decimal(self) -> dict:
        if self.current == 'Error' or self.done:
            self.reset()
        if self.new_input:
            self.current = '0.'
            self.new_input = False
        elif '.' not in self.current:
            self.current += '.'
        self._refresh_expression()
        return self._state()

    # [수행과제] 사칙연산 메서드를 제공한다.
    def add(self) -> dict:
        return self._set_operator('+')

    def subtract(self) -> dict:
        return self._set_operator('-')

    def multiply(self) -> dict:
        return self._set_operator('x')

    def divide(self) -> dict:
        return self._set_operator('÷')

    # [수행과제] 부호 전환과 퍼센트 기능을 처리한다.
    def negative_positive(self) -> dict:
        if self.current == 'Error':
            return self.reset()
        if self.current[0] == '-':
            self.current = self.current[1:]
        else:
            self.current = '-' + self.current
        if self.current == '-0':
            self.current = '0'
        self._refresh_expression()
        return self._state()

    def percent(self) -> dict:
        if self.current == 'Error':
            return self.reset()
        self.current = self._format_number(float(self.current) / 100)
        self._refresh_expression()
        return self._state()

    # [수행과제] 저장된 연산자로 결과를 계산한다.
    def equal(self) -> dict:
        if self.left is None or self.operator is None:
            return self._state()
        result = self._calculate(float(self.current))
        if result is None:
            self.current = 'Error'
            self.expression = ''
        else:
            self._refresh_expression()
            self.current = self._format_number(result)
        self.left = None
        self.operator = None
        self.new_input = True
        self.done = True
        return self._state()

    def _set_operator(self, operator: str) -> dict:
        if self.current == 'Error':
            return self.reset()
        if self.left is not None and not self.new_input:
            result = self._calculate(float(self.current))
            if result is None:
                self.current = 'Error'
                return self._state()
            self.current = self._format_number(result)
        self.left = float(self.current)
        self.operator = operator
        self.expression = self._format_number(self.left) + operator
        self.new_input = True
        self.done = False
        return self._state()

    # [수행과제] dict로 연산을 선택해 사칙연산을 수행한다.
    def _calculate(self, right: float) -> object:
        if self.operator == '÷' and right == 0:
            return None
        operations = {
            '+': lambda: self.left + right,
            '-': lambda: self.left - right,
            'x': lambda: self.left * right,
            '÷': lambda: self.left / right,
        }
        return operations[self.operator]()

    def _refresh_expression(self) -> None:
        if self.left is not None and self.operator:
            left = self._format_number(self.left)
            current = self._format_display(self.current)
            self.expression = left + self.operator + current

    # [수행과제] 화면에 표시할 값을 dict로 반환한다.
    def _state(self) -> dict:
        return {
            'expression': self.expression,
            'display': self._format_display(self.current),
        }

    # [보너스과제] 소수점과 큰 숫자 표시를 정리한다.
    def _format_number(self, number: float) -> str:
        if number == int(number):
            return str(int(number))
        value = str(round(number, 6))
        return value.rstrip('0').rstrip('.') if '.' in value else value

    def _format_display(self, value: str) -> str:
        if value in ('0.', '-0.', 'Error'):
            return value
        if '.' not in value:
            return f'{int(value):,}'
        left, right = value.split('.', maxsplit=1)
        return f'{int(left):,}.{right}'


class CalculatorUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.calculator = Calculator()
        self.init_ui()

    # [수행과제] 아이폰 계산기와 유사한 UI를 만든다.
    def init_ui(self) -> None:
        self.setWindowTitle('Calculator')
        self.setFixedSize(*Config.WINDOW_SIZE)
        self.setStyleSheet(f'background:{Config.BG_COLOR};')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 72, 18, 28)
        self.expression = QLabel('')
        self.display = QLabel('0')
        for label in (self.expression, self.display):
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addStretch()
        layout.addWidget(self.expression)
        layout.addWidget(self.display)
        grid = QGridLayout()
        grid.setSpacing(Config.BTN_GAP)
        self._add_buttons(grid)
        layout.addLayout(grid)
        self._update_display(self.calculator.reset())

    # [수행과제] 설정 데이터로 버튼을 만든다.
    def _add_buttons(self, grid: QGridLayout) -> None:
        for row, buttons in enumerate(Config.BUTTONS):
            for column, text in enumerate(buttons):
                button = QPushButton(text)
                button.setFixedSize(Config.BTN_SIZE, Config.BTN_SIZE)
                button.setStyleSheet(self._style(text))
                button.clicked.connect(
                    lambda checked, value=text: self.on_click(value)
                )
                grid.addWidget(button, row, column)

    def _style(self, text: str) -> str:
        button_type = 'num' if text.isdigit() or text == '.' else 'fn'
        if text in '÷x-+=':
            button_type = 'op'
        bg_color, font_color = Config.COLORS[button_type]
        return Config.BUTTON.format(bg=bg_color, fg=font_color)

    # [수행과제] 버튼 입력과 계산 기능을 연결한다.
    def on_click(self, char: str) -> None:
        actions = {
            '⌫': self.calculator.reset,
            'AC': self.calculator.reset,
            '+/-': self.calculator.negative_positive,
            '%': self.calculator.percent,
            '÷': self.calculator.divide,
            'x': self.calculator.multiply,
            '-': self.calculator.subtract,
            '+': self.calculator.add,
            '=': self.calculator.equal,
            '.': self.calculator.input_decimal,
        }
        action = actions.get(char, lambda: self.calculator.input_number(char))
        self._update_display(action())

    # [수행과제] dict로 받은 식과 결과를 화면에 표시한다.
    def _update_display(self, state: dict) -> None:
        display = state['display']
        size = 56 if len(display) <= 8 else 42
        self.expression.setText(state['expression'])
        self.display.setText(display)
        self.expression.setStyleSheet(Config.EXPRESSION)
        self.display.setStyleSheet(Config.DISPLAY.format(size=size))


if __name__ == '__main__':
    app = QApplication([])
    window = CalculatorUI()
    window.show()
    app.exec()
