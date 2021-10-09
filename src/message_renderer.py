from typing import NamedTuple
from src.message import Message
from src.lib import get_by_path

color = {
    4293271831: "red",
    4293467747: "pink",
    4294278144: "orange",
    4294953512: "yellow",
    4280150454: "green",
    4278248959: "water",
    4280191205: "blue"
}


class MessageRendererTuple(NamedTuple):
    message: str
    authorName: str
    authorExternalChannelId: str
    timestampUsec: str
    timestampText: str
    message_type: str
    purchaseAmountText: str
    bodyBackgroundColor: str
    id: str


class MessageRenderer:
    def __init__(self, item: dict) -> None:
        conv_c = {
            "liveChatTextMessageRenderer": LiveChatText,
            "liveChatPaidMessageRenderer": LiveChatPaid,
            "liveChatMembershipItemRenderer": LiveChatMembership,
            "liveChatViewerEngagementMessageRenderer": LiveChatViewerEngagementMessage,
            "liveChatPaidStickerRenderer": LiveChatPaidSticker,
        }
        self.item = item
        renderer_type = list(item.keys())[0]
        if "showItemEndpoint" in list(item[renderer_type].keys()):
            massage = f"[warn] showItemEndpoint [id] {item[list(item.keys())[0]]['id']}"
            raise KeyError(massage)
        else:
            input = item[renderer_type]
        self.renderer = conv_c[renderer_type](input)


class LiveChatText(MessageRendererTuple):
    def __new__(cls, input: dict) -> MessageRendererTuple:
        params = [
            str(Message(input["message"]["runs"])),
            input["authorName"]["simpleText"],
            input["authorExternalChannelId"],
            input["timestampUsec"],
            input["timestampText"]["simpleText"],
            "LiveChatText",
            "",
            "",
            input["id"]
        ]
        return super().__new__(cls, *params)


class LiveChatPaid(MessageRendererTuple):
    def __new__(cls, input: dict) -> MessageRendererTuple:

        message = str(Message(input["message"]["runs"])
                      ) if "message" in input.keys() else ""
        params = [
            message,
            input["authorName"]["simpleText"],
            input["authorExternalChannelId"],
            input["timestampUsec"],
            input["timestampText"]["simpleText"],
            "LiveChatPaid",
            input["purchaseAmountText"]["simpleText"],
            color[input["bodyBackgroundColor"]],
            input["id"]
        ]
        return super().__new__(cls, *params)


class LiveChatMembership(MessageRendererTuple):
    def __new__(cls, input: dict) -> MessageRendererTuple:
        params = [
            "".join(x["text"] for x in input["headerSubtext"]["runs"]),
            input["authorName"]["simpleText"],
            input["authorExternalChannelId"],
            input["timestampUsec"],
            input["timestampText"]["simpleText"],
            "LiveChatMembership",
            "",
            "",
            input["id"]
        ]
        return super().__new__(cls, *params)


class LiveChatPaidSticker(MessageRendererTuple):
    def __new__(cls, input: dict) -> MessageRendererTuple:

        message = get_by_path(
            input,
            [
                "sticker",
                "accessibility",
                "accessibilityData",
                "label"
            ]
        )
        params = [
            message,
            input["authorName"]["simpleText"],
            input["authorExternalChannelId"],
            input["timestampUsec"],
            input["timestampText"]["simpleText"],
            "LiveChatPaidSticker",
            input["purchaseAmountText"]["simpleText"],
            color[input["moneyChipBackgroundColor"]],
            input["id"]
        ]
        return super().__new__(cls, *params)


class LiveChatViewerEngagementMessage(MessageRendererTuple):
    def __new__(cls, input: dict) -> MessageRendererTuple:
        params = [
            "".join(x["text"] for x in input["message"]["runs"]),
            "YOUTUBE",
            "",
            input["timestampUsec"],
            "0:00",
            "LiveChatViewerEngagementMessage",
            "",
            "",
            input["id"]
        ]
        return super().__new__(cls, *params)
