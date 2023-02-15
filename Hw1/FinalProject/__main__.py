"""Функціональність боту розширяєьться дуже просто
   Створюємо модуль з классом боту який імплементує інтересфейс BotInterface

   from SomeBoot import *
   ....
   BOTS = {
    'AddressBook': AddressBook,
    'SomeBot':SomeBot
    'Exit': None
    }

"""
from Bot import Bot
from AddressBook import *

BOTS = {
    'AddressBook': AddressBook,
    'Exit': None
}
if __name__ == "__main__":
    while True:
        print('-'*57 + '\nHello. I am your assistant. What do i have to work with?:\n' + '-'*57)
        for bot in BOTS:
            if bot == 'Exit':
                print('.....')
            print(bot)
        answer = input('> ')
        if answer.lower() == 'exit':
            break 
        current = BOTS.get(answer, None)
        if current is None:
            print('Bot not found. Try again.Press \'Enter\'')
            input()
            continue
        current = Bot(current)
        current.bot.load("auto_save")

        commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'Exit']
        while True:
            print(current.bot.suggetion())
            action = input('> ').strip().lower()
            if action == 'help':
                format_str = str('{:%s%d}' % ('^',20))
                for command in commands:
                    print(format_str.format(command))
                action = input('> ').strip().lower()
                current.handle(action)
            else:
                current.handle(action)
            if action == 'exit':
                break
