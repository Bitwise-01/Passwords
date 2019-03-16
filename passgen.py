# Date: 02/23/2019
# Author: Mohamed
# Description: A password generator

from time import time


def is_integer(input_string):
    integer_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for char in input_string:
        if char not in integer_list:
            return False
    return True


def is_birthday(input_string):
    if len(input_string) != 10:
        return False

    if input_string.count('-') != 2:
        return False

    if not is_integer(input_string.replace('-', '')):
        return False

    return True


def cases(input_string):
    return [input_string.lower(), input_string.title(), input_string.upper()]


class PassGen:

    def __init__(self):
        self.passwords = []
        self.keywords_words = []
        self.keywords_words_cases = []
        self.keywords_integer = []
        self.keywords_birthday = []
        self.passwords = set()

    def chain_cases(self, case_list, i=0, input_combination=''):
        for case in case_list[i]:
            combination = input_combination + case
            if len(case_list) == (i + 1):
                self.keywords_words_cases.append(combination)
            else:
                self.chain_cases(case_list, i=i + 1, input_combination=combination)

    def collect_keywords(self):

        print('\n'
              ' Please enter keywords associated with the target, e.g. names, numbers, birthdays;\n'
              ' Birthdays have to have the following format: mm-dd-yyyy;\n'
              ' After entering all your keywords, press CTRL + C to generate the password list;\n')

        while True:
            try:
                keyword = input(' > ')
                if len(keyword.replace(' ', '')) == 0:
                    pass
                elif is_integer(keyword):
                    self.keywords_integer.append(keyword)
                elif is_birthday(keyword):
                    self.keywords_birthday.append(keyword)
                else:
                    self.keywords_words.append(keyword)
            except KeyboardInterrupt:
                print('\n')
                break

    def combine_words(self):
        for word in self.keywords_words:

            self.keywords_words_cases.append(word)

            if ' ' in word:
                word_parts = word.split(' ')
                cases_list = []

                for part in word_parts:
                    part_cases = cases(part)
                    cases_list.append(part_cases)

                self.chain_cases(cases_list)

        for word in self.keywords_words_cases:
            self.passwords.add(word)

            for i in range(2100):
                word_number_combinations = [
                    '{}{}'.format(word, i),
                    '{}{}'.format(i, word),
                    '{0}{1}{0}'.format(i, word)
                ]

                for combination in word_number_combinations:
                    self.passwords.add(combination)

            for birthday in self.keywords_birthday:
                birthday_parts = birthday.split('-')
                birthday_month = birthday_parts[0]
                birthday_day = birthday_parts[1]
                birthday_year = birthday_parts[2]

                word_birthday_combinations = [
                    '{}{}'.format(word, birthday_year),
                    '{}{}'.format(birthday_year, word),
                    '{}{}{}{}'.format(word, birthday_day, birthday_month, birthday_year),
                    '{}{}{}{}'.format(word, birthday_month, birthday_day, birthday_year),
                    '{}{}{}{}'.format(word, birthday_year, birthday_month, birthday_day)
                ]

                for combination in word_birthday_combinations:
                    self.passwords.add(combination)

    def generator(self):
        self.collect_keywords()
        self.combine_words()

        password_file_name = 'passwords_' + str(round(time())) + '.txt'
        print(' Passwords Generated: {}'.format(len(self.passwords)))

        with open(password_file_name, 'w+') as password_file:
            for password in sorted(self.passwords):
                password_file.write(password + '\n')

        print(' Passwords written to {}'. format(password_file_name))
        input(' Press any key to exit ...')


if __name__ == '__main__':
    PassGen().generator()
