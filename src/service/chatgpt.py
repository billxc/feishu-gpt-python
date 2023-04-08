#Note: The openai-python library support for Azure OpenAI is in preview.
import logging
import os
import openai
from util.app_config import app_config
from util.logger import gpt_logger
if app_config.IS_AZURE:
  openai.api_type =  "azure" 
  openai.api_base = app_config.AZURE_API_HOST
  openai.api_version = "2023-03-15-preview"
  openai.api_key = app_config.AZURE_API_KEY
else:
  openai.api_key = app_config.OPENAI_KEY

def get_single_response(message, prompt = "You are an AI assistant that helps people find information."):
    return get_chat_response([{"role":"user","content":message}])

def get_chat_response(chat_history, prompt="You are an AI assistant that helps people find information."):
    messages = [{"role": "system", "content": prompt}, *chat_history]
    response = get_gpt_response(messages)
    if "choices" not in response:
        return ""
    choice = response["choices"][0] # type: ignore
    if "message" not in choice:
        return ""
    message = choice["message"]
    if "content" in message and "role" in message and message["role"] == "assistant":
        return message["content"]
    return ""

def get_gpt_response(messages):
    gpt_logger.info("GPT request: %s", messages)
    response = openai.ChatCompletion.create(
      engine=app_config.GPT_MODEL,
      messages=messages,
      stop=None)
    return response

if __name__ == "__main__":
    print(get_chat_response([{"role":"assistant","content":"Hello, how can I help you?"},{"role":"user","content":"Tell me a joke."}]))
    print(get_single_response("什么是战争国债"))