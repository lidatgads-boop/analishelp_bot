from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Уроки по инвестициям", callback_data="menu_education")
    builder.button(text="Пройти квиз", callback_data="menu_quiz")
    builder.button(text="Вопросы и ответы", callback_data="menu_faq")
    builder.button(text="Словарь инвестора", callback_data="menu_glossary")
    builder.adjust(1)
    return builder.as_markup()


WELCOME_TEXT = (
    "Привет! Я финансовый ассистент — ваш помощник в мире инвестиций.\n\n"
    "Здесь вы можете найти:\n"
    "• Образовательные уроки от новичка до опытного инвестора\n"
    "• Квизы для проверки знаний\n"
    "• Ответы на частые вопросы\n"
    "• Глоссарий инвестиционных терминов\n"
    "\n"
    "Все материалы носят исключительно образовательный характер "
    "и не являются инвестиционной рекомендацией."
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "Главное меню\n\nВыбери раздел:",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("education"))
async def cmd_education(message: Message):
    from handlers.education import lessons_keyboard
    await message.answer(
        "Уроки по инвестициям\n\nВыбери урок:",
        reply_markup=lessons_keyboard()
    )


@router.message(Command("quiz"))
async def cmd_quiz(message: Message):
    from aiogram.fsm.context import FSMContext
    from handlers.quiz import QUIZ_QUESTIONS, QuizState, answer_keyboard
    await message.answer(
        f"Квиз: проверь свои знания\n\nВопрос 1 из {len(QUIZ_QUESTIONS)}\n\n{QUIZ_QUESTIONS[0]['question']}",
        reply_markup=answer_keyboard(0)
    )


@router.message(Command("faq"))
async def cmd_faq(message: Message):
    from handlers.faq import faq_keyboard
    await message.answer(
        "Частые вопросы об инвестициях\n\nВыбери вопрос:",
        reply_markup=faq_keyboard()
    )


@router.message(Command("glossary"))
async def cmd_glossary(message: Message):
    from handlers.education import GLOSSARY
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    text = "Словарь инвестора\n\n"
    for term, definition in GLOSSARY.items():
        text += f"{term} — {definition}\n\n"
    builder = InlineKeyboardBuilder()
    builder.button(text="Главное меню", callback_data="main_menu")
    await message.answer(text, reply_markup=builder.as_markup())



@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню\n\nВыбери раздел:",
        reply_markup=main_menu_keyboard()
    )

