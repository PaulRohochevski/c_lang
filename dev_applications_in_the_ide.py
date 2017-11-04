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
