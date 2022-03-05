from aiogram import Bot, Dispatcher, types, executor
import asyncio
import aioschedule
from main import get_fresh_data
from aiogram.utils.markdown import hlink

bot = Bot(token='my_token', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

# тест
async def trial_trip():
    name = 'Hello from Mihal Ivanicha!'
    await bot.send_message('my_id', name, disable_notification=True)
    
    
# вызов функции проверяющей свежие статьи
async def sending_massage(path=get_fresh_data()):
    fresh_new_dict = path
    
    if len(fresh_new_dict) > 0:
        for k, v in fresh_new_dict.items():
            # finifed_message = f"{k} --> {v}"
            finifed_message = f"{hlink(k,v)}"
            await bot.send_message('my_id', finifed_message, disable_notification=True)
            
    else:
        await bot.send_message('my_id', 'No fresh news!!!', disable_notification=True)
    

async def scheduler():
    aioschedule.every(20).seconds.do(trial_trip)
    aioschedule.every(45).seconds.do(sending_massage)
    await asyncio.sleep(5)
    
    while True:
        await aioschedule.run_pending()
        

async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
