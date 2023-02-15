from type_bot_class import BotInterface

class Bot:
    def __init__(self, bot:BotInterface):
        self.bot = bot()

    def handle(self, action):
        if action == 'add':
        
            return self.bot.add()

        elif action == 'search':
            print(self.bot.search()
            )
        elif action == 'edit':        
            return self.bot.edit()

        elif action == 'remove':    
            return self.bot.remove()

        elif action == 'save':
            return self.bot.save()
            
        elif action == 'load':
            return self.bot.load()

        elif action == 'congratulate':
            print(self.bot.congratulate())

        elif action == 'view':
            print(self.bot)

        elif action == 'exit':
            pass
        else:
            print("There is no such command!")
