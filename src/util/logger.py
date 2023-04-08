import logging
import os

# create logs folder if not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

CONSOLE_LOGGING_FORMAT = '%(asctime)s %(levelname)s %(message)s'
FILE_LOGGING_FORMAT = '%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s'

logging.basicConfig(
    format=CONSOLE_LOGGING_FORMAT,
    level=logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(f'logs/{name}.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(FILE_LOGGING_FORMAT))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger

feishu_message_logger = get_logger("feishu_message")
gpt_logger = get_logger("gpt")
app_logger = get_logger("app")

if __name__ == "__main__":
    feishu_message_logger.info("test")
    gpt_logger.info("test")