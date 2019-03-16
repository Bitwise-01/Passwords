# Date: 02/23/2019
# Author: Mohamed
# Description: A password generator


class List:

    def __init__(self):
        self.items = []

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        while len(self.items):
            yield self.items.pop(0)

    def __len__(self):
        return len(self.items)

    def append(self, item, front=False):
        if not item in self.items:
            self.items.append(item)

        for _ in (item.lower(), item.title(), item.upper()):
            if _ in self.items:
                continue

            if front:
                self.items.insert(0, _)
            else:
                self.items.append(_)


class PassGen:

    def __init__(self):
        self.words = []
        self.b_days = []
        self.is_alive = True
        self.password_list = List()
        self.suffix = [_ for _ in range(124)]

    def get_input(self):
        while self.is_alive:
            print(
                'Enter a keyword, name, password, number, symbol, or birthday(mm-dd-yyy)')
            print('To generate a password list enter generate')

            try:
                user_input = str(input('\n$> ')).strip()
            except:
                self.is_alive = False

            if not self.is_alive or not user_input:
                continue

            if user_input.lower() != 'generate':
                self.append_data(user_input)
            else:
                self.generate()
                self.is_alive = False
                continue

            print('\n')

    def append_data(self, data):
        if len(data.split('-')) == 3:  # birthday
            if not data in self.b_days:
                self.b_days.append(data)

        elif data.isdigit():  # number
            if not data in self.suffix:
                self.suffix.insert(0, data)

        elif len([_ for _ in data if _.isdigit()]) == (len(data) - 1):  # float
            if not data in self.suffix:
                self.suffix.insert(0, data)
                self.suffix.insert(0, ''.join(
                    [_ for _ in data if _.isdigit()]))

        elif data.isalpha():  # words
            if not data.lower() in self.words:
                self.words.append(data)

        elif len([_ for _ in data if not _.isalpha() and not _.isdigit()]) == len(data):  # symbol
            if not data in self.suffix:
                self.suffix.insert(0, data)

        else:  # password
            self.password_list.append(data, front=True)

    def generate(self):

        for num in self.suffix:

            for word in self.words:

                self.password_list.append(word)
                self.password_list.append(f'{word}{num}')
                self.password_list.append(f'{num}{word}')
                self.password_list.append(f'{num}{word}{num}')

                for bday in self.b_days:

                    year = bday.split('-')[-1]
                    plain_bday = bday.replace('-', '')

                    self.password_list.append(plain_bday)
                    self.password_list.append(f'{word}{year}')
                    self.password_list.append(f'{word}{year[2:]}')
                    self.password_list.append(f'{word}{plain_bday}')

        with open('pass.txt', 'wt', encoding='utf-8') as output_file:

            print(
                f'Generating a list of {len(self.password_list)} passwords ...')

            for pwd in self.password_list:
                output_file.write(f'{pwd}\n')


if __name__ == '__main__':
    PassGen().get_input()
