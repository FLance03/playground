from typing import Callable

from PyQt5.QtWidgets import QLineEdit

class Computation:
    is_operation = [True]
    result_shown = False
    selections = []
    already_decimal = [False]
    parenthesis_count = 0

    def __init__(self, line_edit:QLineEdit):
        super().__init__()
        self.line_edit = line_edit

    def reset(self):
        self.selections = []
        self.line_edit.clear()
        self.already_decimal = [False]

    def will_reset(self):
        if self.result_shown:
            self.reset()
        self.result_shown = False

    def add_op(self, code, op):
        self.will_reset()
        self.line_edit.insert(code)
        if len(self.selections) > 0 and self.is_operation[-1]:
            self.selections[-1] = op
        else:
            self.selections.append(op)
            self.already_decimal.append(False)
        self.is_operation.append(True)

    def check_if_opening_parenthesis_allowed(self):
        return self.is_operation[-1] or (len(self.selections) > 0 and self.selections[-1] == '(')

    def check_if_closing_parenthesis_allowed(self):
        return self.parenthesis_count > 0 and not self.is_operation[-1] and \
               (len(self.selections) > 0 and self.selections[-1] not in ['.', '('])

    def add_num(self, code):
        self.will_reset()
        try:
            if self.already_decimal[-1] and code == '.':
                raise Exception("Double decimal")
            elif code == ')' and not self.check_if_closing_parenthesis_allowed():
                raise Exception("Too much closing parenthesis")
            elif code == '(' and not self.check_if_opening_parenthesis_allowed():
                raise Exception("Parenthesis after number or parenthesis")
            elif code in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] and \
                    (len(self.selections) > 0 and self.selections[-1] == ')'):
                raise Exception("Number after parenthesis")
        except Exception as e:
            if str(e) in ["Double decimal", "Too much closing parenthesis",
                          "Parenthesis after number or parenthesis", "Number after parenthesis"]:
                print(str(e))
                pass
        else:
            if code == '.':
                self.already_decimal[-1] = True
            elif code == '(':
                self.parenthesis_count += 1
            elif code == ')':
                self.parenthesis_count -= 1
            print(self.parenthesis_count)
            self.line_edit.insert(code)
            self.is_operation.append(False)
            self.selections.append(code)

    def back(self):
        if len(self.line_edit.text()) > 0:
            self.line_edit.setText(self.line_edit.text()[:-1])
            is_operation = self.is_operation.pop()
            code = self.selections.pop()
            if code == '.':
                self.already_decimal[-1] = False
            elif code == '(':
                self.parenthesis_count -= 1
            elif code == ')':
                self.parenthesis_count += 1
            elif isinstance(code, Operator):
                self.already_decimal.pop()

    def erase(self):
        self.reset()

    def calculate(self, compressed_selections):
        def get_parenthesis_end(open_index):
            index = open_index
            if selections_A[open_index] == '(':
                num_open = 1
                while num_open > 0:
                    index += 1
                    if selections_A[index] == '(':
                        num_open += 1
                    elif selections_A[index] == ')':
                        num_open -= 1
            return index

        print('sssssssss', compressed_selections)
        state = 'start'
        op = None
        num = ''
        precedences = list(set([selection.precedence for selection in compressed_selections if isinstance(selection, Operator)]))
        precedences.sort(reverse=True)
        print(precedences)
        selections_A = compressed_selections
        selections_B = []
        for precedence in precedences:
            print('aaa', selections_A)
            selections_A_len = len(selections_A)
            i = 0
            while i < selections_A_len:
                selection = selections_A[i]
                if isinstance(selection, Operator) and i > 0:
                    if selection.precedence == precedence and i+1 < len(selections_A):
                        if selections_A[i + 1] == '(':
                            rhs_end = get_parenthesis_end(i + 1)
                            rhs = self.calculate(selections_A[i + 2:rhs_end])
                        else:
                            rhs_end = i + 1
                            rhs = selections_A[i + 1]
                        selections_A[rhs_end] = selection.op(selections_A[i-1], rhs)
                        i = rhs_end
                    else:
                        selections_B.append(selections_A[i-1])
                        selections_B.append(selection)
                elif selection == '(':
                    start = i + 1
                    end = get_parenthesis_end(i)
                    selections_A[end] = self.calculate(selections_A[start:end])
                    i = end
                i += 1
            # if len(selections_A) >= 3 and isinstance(selections_A[-2], Operator) and selections_A[-2].precedence != precedence:
            selections_B.append(selections_A[-1])
            del selections_A
            selections_A = selections_B[:]
            selections_B = []
        print(selections_A)
        return selections_A[0]

    def compute(self):
        # Make sure all opened parentheses are closed
        while self.parenthesis_count > 0:
            self.add_num(')')
        def compress_selections(selections):
            num = ''
            compressed_selections = []
            for selection in selections:
                try:
                    float(num + selection)
                except:
                    if num != '':
                        compressed_selections.append(float(num))
                        num = ''
                    compressed_selections.append(selection)
                else:
                    num += selection
            if num != '':
                compressed_selections.append(float(num))
            return compressed_selections
        print('hoi', compress_selections(self.selections))
        if len(self.selections) > 0:
            answer = self.calculate(compress_selections(self.selections))
            self.line_edit.setText(str(answer))
            self.result_shown = True


class Operator:
    def __init__(self, op, precedence):
        self.op = op
        self.precedence = precedence


class Operations:
    def get_precedence(self, method):
        if method in [self.add, self.subtract]:
            return 1
        elif method in [self.multiply, self.divide]:
            return 2

    def __add_line_edit(self, addend, line_edit:QLineEdit) -> None:
        print('add')
        # try:
        #     value = float(line_edit.text())
        # except ValueError:
        #     print('Not valid number')
        # else:
        #     line_edit.setText(value + addend)

    # Can include more keyword parameters while only raise exception when one of them is None
    def add(self):
        # print(line_edit)
        # if line_edit is None:
        #     raise Exception('One keyword parameter is required')
        # self.__add_line_edit(addend, line_edit)
        return Operator(lambda a, b: a + b, 1)

    def subtract(self):
        return Operator(lambda a, b: a - b, 1)
        print('subtract')

    def multiply(self):
        return Operator(lambda a, b: a * b, 2)
        print('multiply')

    def divide(self):
        return Operator(lambda a, b: a / b, 2)
        print('divide')

    def CE(self):
        print('CE')

    def C(self):
        print('C')

    def erase(self):
        print('erase')

    def equals(self):
        print('equals')

    def negate(self):
        print('negate')

    def decimal(self):
        print('decimal')

class Numbers:
    def number(self, value:int, line_edit:QLineEdit) -> Callable[[], None]:
        def append_value() -> None:
            print(value)
            # new_text = str(line_edit.text()) + str(value)
            # line_edit.setText(new_text)
        return append_value
