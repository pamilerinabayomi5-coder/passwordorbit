import re

def escape_markdown_v2(text: str) -> str:
    """Escapes markdown v2 reserved formatting symbols."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)
