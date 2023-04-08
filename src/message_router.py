
import json
import attr
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from store.chat_history import ChatEvent, append_chat_event
from handler.command_handler import CommandHandler
from handler.message_handler import MyMessageEventHandler
from util.app_config import app_config
from feishu.feishu_conf import feishu_conf
from util.logger import feishu_message_logger

message_handler = MyMessageEventHandler(app_config,feishu_conf)
command_handler = CommandHandler(app_config,feishu_conf)
def route_im_message(ctx:Context, conf:Config, event: MessageReceiveEvent) -> Any:
    # ignore request if sender_type is not user
    if event.event.sender.sender_type != "user":
        return
    # ignore request if event_type is not im.message.receive_v1
    if event.header.event_type != "im.message.receive_v1":
        return
    feishu_message_logger.info("Feishu message: %s", attr.asdict(event.event))
    # if message content text starts with /, then it is a command
    json_content = json.loads(event.event.message.content)
    if "text" in json_content and json_content["text"].startswith("/"):
        command = event.event.message.content[1:]
        command_handler.handle_message(event)
    else:
        chat_event = ChatEvent(**{
            "user_id": event.event.sender.sender_id.user_id,
            "chat_id": event.event.message.chat_id,
            "chat_type": event.event.message.chat_type,
            "message_id": event.event.message.message_id,
            "message_type": event.event.message.message_type,
            "content": event.event.message.content,
            "create_time": event.event.message.create_time,
            "sender_user_id": event.event.sender.sender_id.user_id
        })
        append_chat_event(chat_event)
        message_handler.handle_message(chat_event)