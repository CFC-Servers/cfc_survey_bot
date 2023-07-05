# Structs for passing data around

from typing import Optional
from interactions.models.discord.enums import ButtonStyle


class OptionStruct:
    def __init__(
            self,
            text: str,
            button_text: Optional[str] = "",

            text_emoji_name: Optional[str] = None,

            button_emoji_name: Optional[str] = None,
            button_emoji_id: Optional[str] = None,

            color: Optional[int] = ButtonStyle.SECONDARY):

        self.text = text
        self.text_emoji_name = text_emoji_name
        self.button_text = button_text
        self.button_emoji_name = button_emoji_name
        self.button_emoji_id = button_emoji_id
        self.color = color


realm_translation = {
    "cfc3": "CFC Build/Kill",
    "cfcrp": "CFC DarkRP",
    "cfcttt": "CFC TTT",
    "discord": "Discord",
    "meta": "Meta",
    "web": "Website",
}
