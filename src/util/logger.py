import logging
import os

# create logs folder if not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

feishu_message_logger = logging.getLogger("feishu_message_logger")
feishu_message_logger.setLevel(logging.DEBUG)
feishu_message_logger.addHandler(logging.FileHandler('logs/feishu_message.log', encoding='utf-8'))

gpt_logger = logging.getLogger("gpt_logger")
gpt_logger.setLevel(logging.DEBUG)
gpt_logger.addHandler(logging.FileHandler('logs/gpt.log', encoding='utf-8'))

if __name__ == "__main__":
    feishu_message_logger.info("test")
    gpt_logger.info("test")