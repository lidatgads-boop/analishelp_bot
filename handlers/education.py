from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

LESSONS = {
    "lesson_1": {
        "title": "Урок 1: Что такое инвестиции?",
        "text": (
            "Инвестиции — это вложение денег или других ресурсов с целью получения дохода в будущем.\n\n"
            "Зачем инвестировать?\n"
            "Деньги со временем обесцениваются из-за инфляции. Инвестиции помогают сохранить и увеличить капитал.\n\n"
            "Основные принципы:\n"
            "• Начинать раньше лучше, чем позже\n"
            "• Диверсификация снижает риски\n"
            "• Чем выше потенциальная доходность — тем выше риск\n\n"
            "Пример:\n"
            "Если положить 100 000 руб. под 10% годовых, через 10 лет это станет ~259 000 руб. — и это без пополнений.\n\n"
            "Материал носит образовательный характер."
        ),
        "pdf": "lesson_1.pdf",
        "pdf_name": "Урок 1 — Что такое инвестиции.pdf"
    },
    "lesson_2": {
        "title": "Урок 2: Виды инвестиций",
        "text": (
            "Основные инструменты инвестирования:\n\n"
            "Банковский вклад\n"
            "Низкий риск, фиксированный доход. Подходит для сбережений на короткий срок.\n\n"
            "Облигации\n"
            "Долговые бумаги. Компания или государство берёт у вас деньги в долг и платит купон (процент).\n\n"
            "Акции\n"
            "Доля в компании. Потенциально высокий доход, но и риск выше.\n\n"
            "Недвижимость\n"
            "Стабильный актив, но требует значительного капитала.\n\n"
            "ETF / Фонды\n"
            "Корзина активов. Отличный способ диверсификации с небольшими вложениями.\n\n"
            "Материал носит образовательный характер."
        ),
        "pdf": "lesson_2.pdf",
        "pdf_name": "Урок 2 — Виды инвестиций.pdf"
    },
    "lesson_3": {
        "title": "Урок 3: Риск и доходность",
        "text": (
            "Риск и доходность — два неразрывных понятия.\n\n"
            "Соотношение риска и доходности:\n"
            "• Вклады в банке: 5–10% годовых, минимальный риск\n"
            "• Облигации: 8–14% годовых, низкий-средний риск\n"
            "• Акции: 10–30%+, высокий риск\n"
            "• Криптовалюта: неограниченный рост/падение, очень высокий риск\n\n"
            "Как управлять рисками:\n"
            "• Не вкладывать все деньги в один актив\n"
            "• Иметь финансовую подушку (3–6 месячных расходов)\n"
            "• Инвестировать только свободные средства\n"
            "• Изучать инструменты перед вложением\n\n"
            "Материал носит образовательный характер."
        ),
        "pdf": "lesson_3.pdf",
        "pdf_name": "Урок 3 — Риск и доходность.pdf"
    },
    "lesson_4": {
        "title": "Урок 4: Как начать инвестировать?",
        "text": (
            "Шаги для старта инвестора:\n\n"
            "1. Создай финансовую подушку\n"
            "Отложи 3–6 месяцев расходов на отдельный счёт.\n\n"
            "2. Определи цель и горизонт\n"
            "Копишь на квартиру за 5 лет или на пенсию за 20? Это влияет на стратегию.\n\n"
            "3. Выбери брокера\n"
            "Открой брокерский счёт или ИИС (индивидуальный инвестиционный счёт) для налоговых льгот.\n\n"
            "4. Начни с простого\n"
            "ETF на индекс — хороший старт. Широкая диверсификация, низкие комиссии.\n\n"
            "5. Инвестируй регулярно\n"
            "Стратегия усреднения (DCA): вкладывай фиксированную сумму каждый месяц.\n\n"
            "Материал носит образовательный характер. Перед инвестированием проконсультируйся с финансовым советником."
        ),
        "pdf": "lesson_4.pdf",
        "pdf_name": "Урок 4 — Как начать инвестировать.pdf"
    },
}

GLOSSARY = {
    "Актив": "Всё, что имеет ценность и может приносить доход: акции, недвижимость, бизнес.",
    "Диверсификация": "Распределение вложений по разным инструментам для снижения риска.",
    "Дивиденды": "Часть прибыли компании, выплачиваемая акционерам.",
    "ИИС": "Индивидуальный инвестиционный счёт — даёт налоговые льготы (до 52 000 руб./год).",
    "Купон": "Регулярный процентный доход по облигации.",
    "Ликвидность": "Скорость, с которой актив можно продать без потери стоимости.",
    "Портфель": "Набор всех инвестиционных активов инвестора.",
    "ETF": "Биржевой фонд — корзина ценных бумаг, торгующаяся как одна акция.",
}


def lessons_keyboard():
    builder = InlineKeyboardBuilder()
    for key, val in LESSONS.items():
        builder.button(text=val["title"], callback_data=f"lesson_{key.split('_')[1]}")
    builder.button(text="Словарь терминов", callback_data="glossary")
    builder.button(text="Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


def lesson_keyboard(lesson_key: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Скачать PDF", callback_data=f"pdf_{lesson_key}")
    builder.button(text="Назад к урокам", callback_data="menu_education")
    builder.button(text="Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


def back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад к урокам", callback_data="menu_education")
    builder.button(text="Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu_education")
async def education_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Уроки по инвестициям\n\nВыбери урок:",
        reply_markup=lessons_keyboard()
    )


@router.callback_query(F.data.startswith("lesson_"))
async def show_lesson(callback: CallbackQuery):
    lesson_key = callback.data
    lesson = LESSONS.get(lesson_key)
    if not lesson:
        await callback.answer("Урок не найден.")
        return
    await callback.message.edit_text(
        f"{lesson['title']}\n\n{lesson['text']}",
        reply_markup=lesson_keyboard(lesson_key)
    )


@router.callback_query(F.data.startswith("pdf_"))
async def send_pdf(callback: CallbackQuery):
    lesson_key = callback.data.replace("pdf_", "")
    lesson = LESSONS.get(lesson_key)
    if not lesson:
        await callback.answer("Файл не найден.")
        return
    try:
        file = FSInputFile(lesson["pdf"], filename=lesson["pdf_name"])
        await callback.message.answer_document(
            document=file,
            caption=f"{lesson['title']}\n\nМатериал носит образовательный характер."
        )
        await callback.answer()
    except Exception:
        await callback.answer("Файл временно недоступен.", show_alert=True)


@router.callback_query(F.data == "menu_glossary")
@router.callback_query(F.data == "glossary")
async def show_glossary(callback: CallbackQuery):
    text = "Словарь инвестора\n\n"
    for term, definition in GLOSSARY.items():
        text += f"{term} — {definition}\n\n"
    builder = InlineKeyboardBuilder()
    builder.button(text="Главное меню", callback_data="main_menu")
    await callback.message.edit_text(text, reply_markup=builder.as_markup())

