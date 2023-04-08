import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import MessageSender
from store.chat_history import clean_chat
from util.logger import app_logger

class CommandHandler:
    def __init__(self, app_config: AppConfig, conf: Config):
        if not app_config:
            raise Exception("app_config is required")
        if not conf:
            raise Exception("conf is required")
        self.app_config = app_config
        self.conf = conf
        self.message_sender = MessageSender(self.conf)

    def handle_message(self, event):
        json_content = json.loads(event.event.message.content)

        if "text" in json_content and json_content["text"].startswith("/"):
            command = json_content["text"][1:]
            if command == "new":
                app_logger.info("new chat")
                clean_chat(event.event.sender.sender_id.user_id)
                self.message_sender.send_text_message(event.event.sender.sender_id.user_id,"New chat started", append=False)
            else:
                app_logger.info("unknown command")
                self.message_sender.send_text_message(event.event.sender.sender_id.user_id, "Unknown command", append=False)
            return True