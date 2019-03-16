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


def is_date(input_string):
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
        self.keywords_integers = []
        self.keywords_dates = []
        self.passwords = set()

    # generate all possible combinations using a list of cases
    def chain_cases(self, case_list, i=0, input_combination=''):
        for case in case_list[i]:
            combination = input_combination + case
            if len(case_list) == (i + 1):
                self.keywords_words_cases.append(combination)
            else:
                self.chain_cases(case_list, i=i + 1, input_combination=combination)

    def collect_keywords(self):

        print('\n'
              ' Please enter keywords associated with the target, e.g. names, numbers, dates (like birthdays);\n'
              ' Dates have to have the following format: mm-dd-yyyy;\n'
              ' After entering all your keywords, press CTRL + C to generate the password list;\n')

        # collect and categorize keywords
        while True:
            try:
                keyword = input(' > ')

                if len(keyword.replace(' ', '')) == 0:
                    pass

                elif is_integer(keyword):
                    self.keywords_integers.append(keyword)

                elif is_date(keyword):
                    self.keywords_dates.append(keyword)

                else:
                    self.keywords_words.append(keyword)

            except KeyboardInterrupt:
                print('\n')
                break

    def combine_words(self):

        # add integers in reverse
        for i in range(len(self.keywords_integers)):
            self.keywords_integers.append(self.keywords_integers[i][::-1])

        # generate all possible case combinations for word and it's parts
        for word in self.keywords_words:
            self.keywords_words_cases.append(word)  # add word
            self.keywords_words_cases.append(word[::-1])  # add word in reverse
            cases_list = []

            if ' ' in word:
                word_parts = word.split(' ')
                self.keywords_words_cases.append(''.join(word_parts)[::-1])  # add word without spaces in reverse

                for part in word_parts:
                    self.keywords_words_cases.append(part)
                    self.keywords_words_cases.append(part[::-1])
                    part_cases = cases(part)
                    cases_list.append(part_cases)

            else:
                word_cases = cases(word)
                cases_list.append(word_cases)

            self.chain_cases(cases_list)

        # add each custom integer as possible password
        for i in self.keywords_integers:
            self.passwords.add(i)

        # generate passwords using all the parts and case combinations
        for word in self.keywords_words_cases:

            # add each word/part/case-combination as password
            self.passwords.add(word)

            # passwords with integers 0-2100 around it
            word_number_combinations = []
            for i in range(2100):
                word_number_combinations += [
                    '{}{}'.format(word, i),
                    '{}{}'.format(i, word),
                    '{0}{1}{0}'.format(i, word)
                ]

            # passwords with custom integers around it
            word_custom_number_combinations = []
            for i in self.keywords_integers:
                word_custom_number_combinations += [
                    '{}{}'.format(word, i),
                    '{}{}'.format(i, word),
                    '{0}{1}{0}'.format(i, word)
                ]

            for combination in (word_number_combinations + word_custom_number_combinations):
                self.passwords.add(combination)

            # passwords with date combinations in them
            for date in self.keywords_dates:
                date_parts = date.split('-')
                data_month = date_parts[0]
                date_day = date_parts[1]
                date_year = date_parts[2]

                word_date_combinations = [
                    '{}{}'.format(word, date_year),
                    '{}{}'.format(date_year, word),
                    '{}{}{}{}'.format(word, date_day, data_month, date_year),
                    '{}{}{}{}'.format(word, data_month, date_day, date_year),
                    '{}{}{}{}'.format(word, date_year, data_month, date_day)
                ]

                for combination in word_date_combinations:
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
