# Date: 02/23/2019
# Author: Mohamed
# Description: A password generator


class PassGen:

    def __init__(self):
        self.pet = None
        self.child = None
        self.spouse = None
        self.target = None 
        self.passwords = []
    
    def prompt(self, txt):
        return str(input(txt))

    def question(self, target):
        answers = {}

        answers['firstname'] = self.prompt('Enter {}\'s first name: '.format(target))
        answers['lastname'] = self.prompt('Enter {}\'s last name: '.format(target))
        answers['nickname'] = self.prompt('Enter {}\'s nick name: '.format(target))

        while True:
            bday = self.prompt('Enter {}\'s birthday (mm-dd-yyyy): '.format(target))

            if not len(bday.strip()):
                break

            if len(bday.split('-')) != 3:
                print('Invalid birthday format\n')
                continue
            
            for _ in bday.split('-'):
                if not _.isdigit():
                    print('Birthday only requires numbers\n')
                    continue
            
            mm, dd, yyyy = bday.split('-')
            
            if int(mm) > 12 or int(dd) > 31 or len(yyyy) != 4:
                print('Invalid birthday\n')
                continue
            
            bday = { 'month': int(mm), 'day': int(dd), 'year': int(yyyy) }
            break 
            
        answers['birthday'] = bday
        return answers   

    def cases(self, word):
        return [word.lower(), word.title()]    

    def format_names(self):                        
        for _ in range(1000):

            for data in [self.target, self.spouse, self.child, self.pet]:

                for n in ['firstname', 'lastname', 'nickname']:

                    name = data[n].strip()

                    if not len(name):
                        continue

                    for word in self.cases(name):

                        a, b, c = ('{}{}'.format(word, _), 
                                  '{}{}'.format(_, word), 
                                  '{0}{1}{0}'.format(_, word)
                                  )

                        if not word in self.passwords:
                            self.passwords.append(word)

                        if not a in self.passwords:
                            self.passwords.append(a)
                        
                        if not b in self.passwords:
                            self.passwords.append(b)

                        if not c in self.passwords:
                            self.passwords.append(c)

                        bday = data['birthday']

                        if bday:
                            d, e, f, g = (
                                '{}{}'.format(word, bday['year']),
                                '{}{}'.format(bday['year'], word),
                                '{}{}{}{}'.format(word, bday['month'], bday['day'], bday['year']),
                                '{}{}{}{}'.format(word, bday['day'], bday['month'], bday['year'])
                            )

                            if not d in self.passwords:
                                self.passwords.append(d)
                            
                            if not e in self.passwords:
                                self.passwords.append(e)
                            
                            if not f in self.passwords:
                                self.passwords.append(f)

                            if not g in self.passwords:
                                self.passwords.append(g)      
        
    def generator(self):
        self.target = self.question('target')  
        print('\n')

        self.spouse = self.question('spouse')
        print('\n')

        self.child = self.question('child')
        print('\n')

        self.pet = self.question('pet')
        print('\n')
        
        self.format_names()

        output_file = '{}.txt'.format(self.target['firstname'].lower()
                             if self.target['firstname'] else 'pass.txt')
        
        with open(output_file, 'wt') as f:
            for pwd in self.passwords:
                f.write('{}\n'.format(pwd))

        print('Passwords Generated: {}'. format(len(self.passwords)))

if __name__ == '__main__':
    PassGen().generator()