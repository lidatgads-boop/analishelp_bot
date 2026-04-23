from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

FAQS = {
    "faq_1": {
        "q": "С какой суммы можно начать инвестировать?",
        "a": (
            "Начать можно с любой суммы — некоторые ETF стоят от 1 руб. "
            "Рекомендуется начинать с суммы, потерю которой вы не почувствуете критично. "
            "Главное — регулярность, а не размер вложений.\n\n"
            "Это образовательная информация, не инвестиционная рекомендация."
        )
    },
    "faq_2": {
        "q": "Нужно ли платить налоги с инвестиций?",
        "a": (
            "Да. В России с дохода от инвестиций удерживается НДФЛ 13% (или 15% при доходе свыше 5 млн руб./год). "
            "Брокер обычно является налоговым агентом — он сам рассчитывает и удерживает налог. "
            "ИИС типа А или Б позволяет получить налоговые льготы.\n\n"
            "Проконсультируйтесь с налоговым консультантом для вашей ситуации."
        )
    },
    "faq_3": {
        "q": "Как выбрать брокера?",
        "a": (
            "При выборе брокера обратите внимание на:\n"
            "• Лицензию ЦБ РФ\n"
            "• Комиссии за сделки и обслуживание\n"
            "• Наличие мобильного приложения\n"
            "• Доступные инструменты\n"
            "• Репутацию и отзывы\n\n"
            "Это образовательная информация, не рекомендация конкретного брокера."
        )
    },
    "faq_4": {
        "q": "Что такое ребалансировка портфеля?",
        "a": (
            "Ребалансировка — приведение портфеля к изначально заданным пропорциям. "
            "Например, если акции выросли и теперь занимают 80% вместо 60%, вы продаёте часть акций "
            "и докупаете облигации. Обычно проводится 1–2 раза в год.\n\n"
            "Это образовательная информация, не инвестиционная рекомендация."
        )
    },
    "faq_5": {
        "q": "Безопасно ли инвестировать онлайн?",
        "a": (
            "Да, если пользоваться лицензированными брокерами с лицензией ЦБ РФ. "
            "Активы на брокерском счёте защищены законодательством. "
            "Остерегайтесь нелицензированных платформ и обещаний гарантированной высокой доходности.\n\n"
            "Всегда проверяйте лицензию на сайте ЦБ РФ: cbr.ru"
        )
    },
}


def faq_keyboard():
    builder = InlineKeyboardBuilder()
    for key, val in FAQS.items():
        builder.button(text=val['q'], callback_data=key)
    builder.button(text="Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


def back_faq_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад к FAQ", callback_data="menu_faq")
    builder.button(text="Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "menu_faq")
async def faq_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Частые вопросы об инвестициях\n\nВыбери вопрос:",
        reply_markup=faq_keyboard()
    )


@router.callback_query(F.data.startswith("faq_"))
async def show_faq(callback: CallbackQuery):
    faq = FAQS.get(callback.data)
    if not faq:
        await callback.answer("Вопрос не найден.")
        return
    await callback.message.edit_text(
        f"{faq['q']}\n\n{faq['a']}",
        reply_markup=back_faq_keyboard()
    )
