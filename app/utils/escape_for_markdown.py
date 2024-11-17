import re


def escape_markdown(text: str) -> str:
    '''
    https://core.telegram.org/bots/api#formatting-options
    '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
    must be escaped with the preceding character '\'.
    '''
    special_chars = r"[\_\*\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\!]"
    return re.sub(special_chars, r"\\\g<0>", text)
