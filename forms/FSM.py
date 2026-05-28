from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    first_int = State()
    second_int = State()
    ai_quesion = State()
    qr_url = State()
    audio_text = State()
    audio_lang = State()
    cur_1 = State()
    cur_2 = State()
    money = State()
    message_id_int_to_delete = State()
    message_id_qr_delete = State()
    message_id_audio_delete = State()
    message_for_admin_delete = State()

class Admin(StatesGroup):
    pass