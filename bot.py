from aiogram import Dispatcher, Bot, executor
import sys

class CPBot:
    def __init__(self, TOKEN_API, storage):
        print("[ ] Initializing Bot...")
        try:
            self.CPbot = Bot(token=TOKEN_API)
            self.dp = Dispatcher(self.CPbot, storage=storage) 
            print("[+] Started succesfully!")
        except Exception as Err:
            print("[ERROR] ", Err)
            sys.exit(1)
    def _start_(self):
        executor.start_polling(self.dp)



        
