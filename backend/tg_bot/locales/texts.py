MESSAGES = {
    'ru': {
        'welcome': "Привет, {name}! 🌟\n\nДобро пожаловать в наш сервис. Жми кнопку ниже, чтобы открыть приложение и начать выполнять задания!",
        'btn_app': "Открыть Web App 🚀"
    },
    'en': {
        'welcome': "Hello, {name}! 🌟\n\nWelcome to our service. Click the button below to open the app and start completing tasks!",
        'btn_app': "Open Web App 🚀"
    }
}

def get_text(lang_code: str, key: str) -> str:
    #check lenguage, default eng
    lang = 'ru' if lang_code == 'ru' else 'en'
    return MESSAGES[lang][key]