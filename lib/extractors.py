"""文本抽取模块：从不同文件类型提取纯文本 (UTF-8 string)"""

import io
from pathlib import Path

from docx import Document
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup


class ExtractionError(Exception):
    """文件无法解析为文本时的错误"""
    pass


def extract_txt(content: bytes) -> str:
    """从 .txt 或 .md 文件提取文本"""
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = content.decode("gbk")
        except UnicodeDecodeError:
            text = content.decode("utf-8", errors="replace")
    return text.strip()


def extract_pdf(content: bytes) -> str:
    """从 PDF 提取文本（仅限可直接提取文本的 PDF，不处理扫描版）"""
    try:
        reader = PdfReader(io.BytesIO(content))
        parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        text = "\n".join(parts).strip()
        if not text:
            raise ExtractionError("该 PDF 无法解析为文本（可能是扫描版）")
        return text
    except Exception as e:
        if isinstance(e, ExtractionError):
            raise
        raise ExtractionError(f"该文件无法解析为文本: {e}")


def extract_docx(content: bytes) -> str:
    """从 .docx 提取文本"""
    try:
        doc = Document(io.BytesIO(content))
        parts = [p.text for p in doc.paragraphs]
        text = "\n".join(parts).strip()
        if not text:
            raise ExtractionError("该 DOCX 无法解析为文本")
        return text
    except Exception as e:
        if isinstance(e, ExtractionError):
            raise
        raise ExtractionError(f"该文件无法解析为文本: {e}")


def extract_html(content: bytes) -> str:
    """从 .html 提取纯文本"""
    try:
        html = content.decode("utf-8", errors="replace")
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        if not text:
            raise ExtractionError("该 HTML 无法解析为文本")
        return text
    except Exception as e:
        if isinstance(e, ExtractionError):
            raise
        raise ExtractionError(f"该文件无法解析为文本: {e}")


EXTRACTORS = {
    ".txt": extract_txt,
    ".md": extract_txt,
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".html": extract_html,
    ".htm": extract_html,
}


def extract_text(content: bytes, filename: str) -> str:
    """
    根据文件扩展名选择抽取方式，返回 UTF-8 字符串。
    若扩展名不支持或抽取失败，抛出 ExtractionError。
    """
    ext = Path(filename).suffix.lower()
    if ext not in EXTRACTORS:
        raise ExtractionError(f"不支持的文件类型: {ext or '(无扩展名)'}")
    return EXTRACTORS[ext](content)
