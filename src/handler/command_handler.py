import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import MessageSender

from store.chat_history import clean_chat

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
            print(command)
            if command == "new":
                print("new chat")
                clean_chat(event.event.sender.sender_id.user_id)
                self.message_sender.send_text_message_no_append(event.event.sender.sender_id.user_id,"New chat started")
