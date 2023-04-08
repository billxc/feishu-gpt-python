import json
import time
import attr
import attrs
from larksuiteoapi.api import Request, set_timeout
from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_FEISHU, LEVEL_DEBUG
from util.app_config import app_config
from store.chat_history import ChatEvent, append_chat_event



@attr.s
class Message(object):
    message_id = attr.ib(type=str) # type: ignore

class MessageSender:
    def __init__(self, conf: Config):
        if not conf:
            raise Exception("conf is required")
        self.conf = conf

    def send_text_message_no_append(self,user_id,msg):
        body = {
            "user_id": user_id,
            "msg_type": "text",
            "content": {
                "text": msg
            }
        }
        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                    output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)

        if resp.code == 0:
            # store the message in the chat history
            new_chat_event = ChatEvent(**{
                "user_id": user_id,
                "chat_id": "",
                "chat_type": "",
                "message_id": resp.data.message_id,
                "message_type": "",
                "content": json.dumps({"text": msg}),
                "sender_user_id": "assistant",
                "create_time": int(time.time())
            })
            print(attrs.asdict(new_chat_event))
            print(resp.data.message_id)
        else:
            print(resp.msg)
            print(resp.error)

    def send_text_message(self,user_id,msg):
        body = {
            "user_id": user_id,
            "msg_type": "text",
            "content": {
                "text": msg
            }
        }
        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                    output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)

        if resp.code == 0:
            # store the message in the chat history
            new_chat_event = ChatEvent(**{
                "user_id": user_id,
                "chat_id": "",
                "chat_type": "",
                "message_id": resp.data.message_id,
                "message_type": "",
                "content": json.dumps({"text": msg}),
                "sender_user_id": "assistant",
                "create_time": int(time.time())
            })
            print(attrs.asdict(new_chat_event))
            append_chat_event(new_chat_event)
            print(resp.data.message_id)
        else:
            print(resp.msg)
            print(resp.error)

    def test_send_message_complex(self):
        body = {
            "user_id": "ab1cd2ef",
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "[飞书](https://www.feishu.cn)整合即时沟通、日历、音视频会议、云文档、云盘、工作台等功能于一体，成就组织和个人，更高效、更愉悦。"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "value": {"value": 1, "value2": "str"},
                                "text": {
                                    "tag": "plain_text",
                                    "content": "主按钮"
                                },
                                "type": "primary"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "次按钮"
                                },
                                "type": "default"
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "危险按钮"
                                },
                                "type": "danger"
                            }
                        ]
                    }
                ]
            }
        }

        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                    output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(conf)
        print('header = %s' % resp.get_header().items())
        print('request id = %s' % resp.get_request_id())
        print(resp)
        if resp.code == 0:
            print(resp.data.message_id)
        else:
            print(resp.msg)
            print(resp.error)

if __name__ == '__main__':
    app_config.validate()
    app_settings = Config.new_internal_app_settings_from_env()
    conf = Config(DOMAIN_FEISHU, app_settings, log_level=LEVEL_DEBUG)
    message_sender = MessageSender(conf)
    message_sender.test_send_message_complex()
    message_sender.send_text_message("ab1cd2ef","Hello World")