from typing import Optional
from interactions.client.enums import ButtonStyle


class OptionStruct:
    def __init__(
            self,
            text: str,
            text_emoji: Optional[str] = None,
            button_text: Optional[str] = "",
            button_emoji: Optional[str] = None,
            color: Optional[int] = ButtonStyle.PRIMARY):

        self.text = text
        self.text_emoji = text_emoji
        self.button_text = button_text
        self.button_emoji = button_emoji
        self.color = color
