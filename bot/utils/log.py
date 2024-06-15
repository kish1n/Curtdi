import logging
import os

# Создание директории для логов, если ее нет
if not os.path.exists('logs'):
    os.makedirs('logs')

# Настройка логирования в файл
log_format = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format, handlers=[
    logging.FileHandler("logs/bot.log", encoding='utf-8'),
    logging.StreamHandler()
])

# Создание отдельных обработчиков для информационных и ошибок
file_handler_info = logging.FileHandler('logs/bot_info.log', encoding='utf-8')
file_handler_info.setLevel(logging.INFO)
file_handler_info.setFormatter(logging.Formatter(log_format))

file_handler_error = logging.FileHandler('logs/bot_error.log', encoding='utf-8')
file_handler_error.setLevel(logging.ERROR)
file_handler_error.setFormatter(logging.Formatter(log_format))

# Настройка основного логгера
logger = logging.getLogger()
logger.addHandler(file_handler_info)
logger.addHandler(file_handler_error)
