from chatbot import ChatBot
from imagebot import ImageBot
from qabot import DocQABot
from querybot import QueryBot
from simplebot import SimpleBot
from typing import Any, Union
import json

import devtools

def instantiate_from_json(json_str: str) -> dict[str, Union[ChatBot, ImageBot, DocQABot, QueryBot, SimpleBot]]:
    """
    Given a JSON string, instantiate the bots and return a dictionary of the instances
    :param json_str: JSON string of the dictionary of bot instances
    :return: Dictionary of bot instances
    """
    data = json.loads(json_str)  # Assuming json_str is a JSON string of the dictionary
    instances = {}

    for instance_name in data:
        params = data[instance_name]
        instance_type = params['type']
        devtools.pprint(instance_name)
        devtools.pprint(instance_type)
        devtools.pprint(params)
        del params['type']

        if instance_type == 'ChatBot':
            instance = ChatBot(**params)
        elif instance_type == 'ImageBot':
            instance = ImageBot(**params)
        elif instance_type == 'DocQABot':
            instance = DocQABot(**params)
        elif instance_type == 'QueryBot':
            instance = QueryBot(**params)
        elif instance_type == 'SimpleBot':
            instance = SimpleBot(**params)
        else:
            raise ValueError(f"Unknown type {instance_type}")

        instances[instance_name] = instance

    return instances

jparms ="""
{

  "x1": {
    "type": "SimpleBot",
    "system_prompt": "Be concise and informative",
    "temperature": 0,
    "model_name": "mistral/mistral-medium",
    "stream_target": "stdout",
    "json_mode": false,
    "api_key": null,
    "mock_response": null
  },
  "x2": {
    "type": "SimpleBot",
    "system_prompt": "Be concise and informative",
    "temperature": 0,
    "model_name": "openai/gpt-3.5-turbo",
    "stream_target": "stdout",
    "json_mode": false,
    "api_key": null,
    "mock_response": null
  }
}
"""

x = instantiate_from_json(jparms)
print(x)
for id in x:
    print("-------------------")
    print(id)
    zz=x[id]("who are you and where are you from? what is your name?")
    print(999,type(zz))
    #print(x[id]("who are you and where are you from? what is your name?"))
