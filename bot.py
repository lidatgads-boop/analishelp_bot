import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, education, quiz, faq

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8010020077:AAHWOIW-z3ajvhO2ZV3BgiDNLp-AX-crn54"

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(common.router)
    dp.include_router(education.router)
    dp.include_router(quiz.router)
    dp.include_router(faq.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
