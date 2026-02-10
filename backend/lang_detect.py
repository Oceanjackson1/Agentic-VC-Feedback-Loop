"""简单语言检测：判断文本是否 primarily 英文"""


def is_primarily_english(text: str) -> bool:
    """
    根据 CJK 字符占比判断文本是否主要为英文。
    若 CJK 占比低于阈值，则认为是英文原文。
    """
    if not text or not text.strip():
        return False
    cjk_count = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    total = len(text.replace(" ", "").replace("\n", ""))
    if total == 0:
        return False
    cjk_ratio = cjk_count / total
    return cjk_ratio < 0.1
