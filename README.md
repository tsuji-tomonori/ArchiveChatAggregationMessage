# ArchiveChatAggregationMessage

```
d["continuationContents"]["liveChatContinuation"]["actions"]
```

- 例外発生するケースあり
  ⇒ 最後(データがない)ケース データを捨ててしまってOK
- これはリストであるため件数分だけループさせる必要あり

---

```
d["continuationContents"]["liveChatContinuation"]["actions"][]["clickTrackingParams"]
```

広告系? 不要そう

---

```
d["continuationContents"]["liveChatContinuation"]["actions"][]["replayChatItemAction"]
```

以下2つある

- actions
  以降その他もろもろ
- videoOffsetTimeMsec
  該当配信時間?

どちらも必ず存在した

---

```
d["continuationContents"]["liveChatContinuation"]["actions"][]["replayChatItemAction"]["actions"]
```

必ず1つ

---

```
d["continuationContents"]["liveChatContinuation"]["actions"][]["replayChatItemAction"]["actions"][0]
```

- addChatItemAction
  通常系(スーパーチャットしているものもある)
- addLiveChatTickerItemAction
  スーパーチャット系 ⇒ 内容の構造が少し複雑
- clickTrackingParams
  広告系?

以降の内容を取得する際は例外処理または分岐処理が必須

## 通常系

```
addChatItemAction
```

- item
- clientId

基本は両方出るが絶対ではない
(ちょくちょくclientIdがない)

item は必ずある

---

```
addChatItemAction["item"]
```

- liveChatPaidMessageRenderer
- liveChatTextMessageRenderer

どちらかがある形

```
addChatItemAction["item"]["liveChatTextMessageRenderer"]
```

- authorBadges
- authorExternalChannelId
- authorName
- authorPhoto
- contextMenuAccessibility
- contextMenuEndpoint
- id
- message
- timestampText
- timestampUsec

authorBadgesは無いときもあり
それ以外はありそう

### authorBadges

```
authorBadges[0]
└liveChatAuthorBadgeRenderer
    ├customThumbnail
    │  └thumbnails[]
    │      └url: str
    ├tooltip: str
    └accessibility
        └accessibilityData
             └label: str
```

Actionしたユーザーのメンバーシップにまつわる情報
入っていなければこの項目自体なさそう

### authorExternalChannelId

文字列

ActionしたユーザーのチャンネルID

### authorName

```
authorName
└simpleText
```

Actionしたユーザー名

### authorPhoto

```
authorPhoto
└thumbnails[]
    ├url: str
    ├width: int
    └height: int
```

Actionしたユーザーのサムネイル画像情報

### contextMenuAccessibility

```
contextMenuAccessibility
└accessibilityData
   └label: str
```

「コメントの操作」が返ってくる

### contextMenuEndpoint

```
contextMenuEndpoint
├commandMetadata
│  └webCommandMetadata
│      └ignoreNavigation: bool
└liveChatItemContextMenuEndpoint
    └params: str
```

何に使用するか不明

### id

文字列

何のIDかは不明 (各Actionごと?)

### message

```
message
└runs[]
    ├text: str
    └emoji
        ├emojiId: str
        ├shortcuts[str]
        ├searchTerms[str]
        ├image
        │  ├thumbnails[]
        │  │  ├url: str
        │  │  ├width: str
        │  │  └height: str
        │  └accessibility
        │      └accessibilityData
        │          └label: str
        └isCustomEmoji: bool
```

チャット欄のメッセージ or 絵文字(メンバーシップ用のみ?)

両方の場合も, どちらか片方の場合もありうる  

### timestampText

```
timestampText
└simpleText: str
```

タイムスタンプ
"HH:MM:DD" 形式

### timestampUsec

文字列

ActionがあったUNIX時間(マイクロ秒)

