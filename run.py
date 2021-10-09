from pathlib import Path
from src.lib import get_by_path, read_json, write_csv
from src.message_renderer import MessageRenderer


def handler(dir_path: Path, output_file: Path) -> None:
    data = []
    files = [file for file in dir_path.iterdir() if file.suffix in [".json"]]
    for file in files:
        try:
            _data = controller(file)
            data += _data
        except KeyError as ke:
            print(ke)
            continue
    header = [
        "message",
        "authorName",
        "authorExternalChannelId",
        "timestampUsec",
        "timestampText",
        "message_type",
        "purchaseAmountText",
        "bodyBackgroundColor"
    ]
    write_csv(header, data, output_file)


def controller(path: Path) -> list:
    input = read_json(path)
    actions = get_by_path(
        input,
        [
            "continuationContents",
            "liveChatContinuation",
            "actions"
        ]
    )
    res = []
    for action in actions:
        try:
            res.append(service(action))
            print("fin this record")
        except KeyError as ke:
            print(f"skip this record. reason: {ke}")
    return res


def service(action: dict) -> list:
    action = get_by_path(
        action,
        [
            "replayChatItemAction",
            "actions"
        ]
    )[0]
    renderer = MessageRenderer(get_action(action)["item"]).renderer
    return list(renderer)


def get_action(action: dict) -> dict:
    res = action.get("addChatItemAction", action.get(
        "addLiveChatTickerItemAction"))
    if res is None:
        raise KeyError("Not addChat*Action.")
    return res


if __name__ == "__main__":
    input_dir = Path(
        r"C:\Users\20160\Desktop\prog\ArchiveChatAggregation\output\eeMWRfqONNc")
    output_file = Path.cwd() / "eeMWRfqONNc.csv"
    handler(input_dir, output_file)
