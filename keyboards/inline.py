from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def destonation_at_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Москва")
    kb.button(text="Санкт-Петербург")
    kb.button(text="Сочи")
    kb.button(text="Калининград")
    kb.button(text="Стамбул")
    kb.button(text="Ереван")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def destonation_to_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Москва")
    kb.button(text="Санкт-Петербург")
    kb.button(text="Сочи")
    kb.button(text="Калининград")
    kb.button(text="Стамбул")
    kb.button(text="Ереван")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def departure_to_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="7 дней")
    kb.button(text="10 дней")
    kb.button(text="14 дней")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
