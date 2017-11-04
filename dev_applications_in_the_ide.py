"""
lab #1 task #21
Вывести на экран 1 или 0 в зависимости от того, есть ли среди первых трех цифр дробной части заданного положительного
вещественного числа цифра нуль.
"""


def zero_detector(real_num: float) -> int:
    real_str = str(real_num)
    dot = real_str.find('.')
    after_dot = real_str[dot + 1:]
    char_index = 0
    for char in after_dot:
        char_index += 1
        if (char == '0') and (char_index < 4):
            print('Detected zero in real between 1 and 3 position after dot: {}'.format(real_str))
            return 1
        elif char_index > 3:
            print('No zero in real between 1 and 3 position after dot: {}'.format(real_str))
            return 0


zero_detector(35.16907)
zero_detector(192.98097)
zero_detector(0.356790)

"""
lab #2 task #21
В старояпонском календаре был принят 60-летний цикл, состоявший из пяти 12-летних подциклов. Подциклы обозначались 
названиями цвета:  green (зеленый), red (красный), yellow (желтый), white (белый), black (черный). Внутри каждого 
подцикла годы носили названия животных: крысы, коровы, тигра, зайца, дракона, змеи, лошади, овцы, обезьяны, курицы, 
собаки и свиньи. (1984 год- год зеленой крысы -был началом очередного цикла). Разработать программу, которая вводит 
номер некоторого года нашей эры и выводит его название по старояпонскому календарю.
"""


class JapanCalendar(object):
    def __init__(self, fixed_date):
        self.first_iter: tuple = ('green', 'red', 'yellow', 'white', 'black')
        self.second_iter: tuple = (
            'rat', 'cow', 'tiger', 'hare', 'dragon', 'snake', 'horse', 'sheep', 'monkey', 'chicken', 'dog', 'pig')
        self.date_of_new_period: int = 1984
        self.current_index: int = 0
        self.fixed_date: int = int(fixed_date)
        self.time_delta: int = self.fixed_date - self.date_of_new_period

    def japan_calendar(self) -> int:

        while self.time_delta < 0:
            self.date_of_new_period -= 60
            self.time_delta = self.fixed_date - self.date_of_new_period

        while self.time_delta >= 60:
            self.date_of_new_period += 60
            self.time_delta = self.fixed_date - self.date_of_new_period

        if 0 <= self.time_delta < 60:
            for f in self.first_iter:
                for s in self.second_iter:
                    if self.current_index == self.time_delta:
                        print('{} is a year of {} {}'.format(self.fixed_date, f, s))
                        return 0
                    self.current_index += 1


JapanCalendar(2017).japan_calendar()
JapanCalendar(1017).japan_calendar()
JapanCalendar(3017).japan_calendar()

"""
lab #3 task #21
Дано n вещественных чисел. Определить, образуют ли они возрастающую последовательность.
"""

sample_1 = (12.3, 15.3, 35.4, 45.7, -16.9, -23.4)
sample_2 = (-16.9, -23.4, 35.4, 12.3, 45.7, 15.3)
sample_3 = (-23.4, -16.9, 12.3, 15.3, 35.4, 45.7)


def sequence(sample: tuple) -> int:
    increased = True
    for i in range(1, len(sample)):
        if sample[i - 1] < sample[i]:
            continue
        else:
            increased = False

    if increased:
        print('{} is increasing sequence'.format(sample))
        return 0
    elif not increased:
        print('{} is not increasing sequence'.format(sample))
        return 0


sequence(sample_1)
sequence(sample_2)
sequence(sample_3)
