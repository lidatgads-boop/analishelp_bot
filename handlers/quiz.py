from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

QUIZ_QUESTIONS = [
    {
        "question": "❓ Что такое диверсификация?",
        "options": [
            "Вложение всех денег в один актив",
            "Распределение вложений по разным инструментам",
            "Продажа активов при падении рынка",
            "Тип банковского вклада",
        ],
        "correct": 1,
        "explanation": "✅ Диверсификация — распределение средств по разным активам для снижения риска."
    },
    {
        "question": "❓ Что такое ИИС?",
        "options": [
            "Иностранный инвестиционный счёт",
            "Индивидуальный инвестиционный счёт",
            "Инструмент инвестиционного страхования",
            "Индекс инвестиционных ставок",
        ],
        "correct": 1,
        "explanation": "✅ ИИС — индивидуальный инвестиционный счёт. Даёт налоговые льготы до 52 000 ₽/год."
    },
    {
        "question": "❓ Какой инструмент наименее рискованный?",
        "options": [
            "Акции роста",
            "Криптовалюта",
            "Банковский вклад",
            "Фьючерсы",
        ],
        "correct": 2,
        "explanation": "✅ Банковский вклад — наименее рискованный инструмент, доход гарантирован в пределах страховки АСВ."
    },
    {
        "question": "❓ Что такое дивиденды?",
        "options": [
            "Комиссия брокера",
            "Купон по облигации",
            "Часть прибыли компании, выплачиваемая акционерам",
            "Налог на доход от инвестиций",
        ],
        "correct": 2,
        "explanation": "✅ Дивиденды — выплата части прибыли компании её акционерам."
    },
    {
        "question": "❓ ETF — это...",
        "options": [
            "Электронный торговый форум",
            "Биржевой фонд — корзина активов",
            "Тип срочного вклада",
            "Европейский торговый франк",
        ],
        "correct": 1,
        "explanation": "✅ ETF (Exchange-Traded Fund) — биржевой фонд, объединяющий множество активов."
    },
]


class QuizState(StatesGroup):
    answering = State()


def answer_keyboard(q_index: int):
    question = QUIZ_QUESTIONS[q_index]
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(question["options"]):
        builder.button(text=option, callback_data=f"quiz_answer_{q_index}_{i}")
    builder.adjust(1)
    return builder.as_markup()


def quiz_result_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Пройти ещё раз", callback_data="menu_quiz")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.answering)
    await state.update_data(q_index=0, score=0)
    q = QUIZ_QUESTIONS[0]
    await callback.message.edit_text(
        f"🧠 <b>Квиз: проверь свои знания</b>\n\nВопрос 1 из {len(QUIZ_QUESTIONS)}\n\n{q['question']}",
        parse_mode="HTML",
        reply_markup=answer_keyboard(0)
    )


@router.callback_query(F.data.startswith("quiz_answer_"), QuizState.answering)
async def process_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    q_index = int(parts[2])
    user_answer = int(parts[3])

    data = await state.get_data()
    score = data.get("score", 0)

    question = QUIZ_QUESTIONS[q_index]
    is_correct = user_answer == question["correct"]
    if is_correct:
        score += 1

    result_icon = "✅" if is_correct else "❌"
    result_text = f"{result_icon} {'Верно!' if is_correct else 'Неверно.'}\n{question['explanation']}"

    next_index = q_index + 1

    if next_index < len(QUIZ_QUESTIONS):
        await state.update_data(q_index=next_index, score=score)
        next_q = QUIZ_QUESTIONS[next_index]
        builder = InlineKeyboardBuilder()
        builder.button(text="➡️ Следующий вопрос", callback_data=f"quiz_next_{next_index}")
        text = (
            f"{result_text}\n\n"
            f"Вопрос {next_index + 1} из {len(QUIZ_QUESTIONS)}\n\n{next_q['question']}"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=answer_keyboard(next_index))
    else:
        await state.clear()
        total = len(QUIZ_QUESTIONS)
        pct = round(score / total * 100)
        if pct == 100:
            grade = "🏆 Отличный результат! Ты настоящий инвестор!"
        elif pct >= 60:
            grade = "👍 Хороший результат! Есть куда расти."
        else:
            grade = "📚 Рекомендуем повторить уроки."

        await callback.message.edit_text(
            f"{result_text}\n\n"
            f"🎯 <b>Квиз завершён!</b>\n\n"
            f"Результат: <b>{score} из {total}</b> ({pct}%)\n{grade}\n\n"
            f"<i>⚠️ Материалы носят образовательный характер.</i>",
            parse_mode="HTML",
            reply_markup=quiz_result_keyboard()
        )
