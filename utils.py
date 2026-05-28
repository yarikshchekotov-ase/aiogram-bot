'''утилиты проекта'''

def split_message(text, max_length=4096):
    return [[text[i:i+max_length]] for i in range(0, len(text), max_length)]

def validator_currency(currency):
    match currency:
        case '🇷🇺':
            currency = 'RUB'
        case '🇺🇸':
            currency = 'USD'
        case '🇪🇺':
            currency = 'EUR'
        case '🇬🇧':
            currency = 'GBP'

    return currency


