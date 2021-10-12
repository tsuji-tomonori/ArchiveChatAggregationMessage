from typing import NamedTuple
from distutils.util import strtobool
import os

IS_TEXT_OUTPUT = strtobool(os.getenv("IS_TEXT_OUTPUT", "true"))
IS_EMOJI_OUTPUT = strtobool(os.getenv("IS_EMOJI_OUTPUT", "true"))


class MessageTuple(NamedTuple):
    message: str


class Message:
    def __init__(self, runs: list) -> None:
        conv_c = {
            "text": Text,
            "emoji": Emoji
        }
        self.runs = runs
        self.message_lst = [conv_c[list(x.keys())[0]](x).message for x in runs]

    def __str__(self) -> str:
        return " ".join(self.message_lst)


class Text(MessageTuple):
    def __new__(cls, input: dict) -> MessageTuple:
        if IS_TEXT_OUTPUT:
            return super().__new__(cls, input["text"])
        else:
            return super().__new__(cls, "")


class Emoji(MessageTuple):
    def __new__(cls, input: dict) -> MessageTuple:
        if IS_EMOJI_OUTPUT:
            return super().__new__(cls, input["emoji"]["shortcuts"][-1])
        else:
            return super().__new__(cls, "")
