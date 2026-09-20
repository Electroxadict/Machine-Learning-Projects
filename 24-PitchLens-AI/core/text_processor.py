"""
Text Processor Module for PitchLens AI
Handles document loading (TXT, PDF, DOCX), text cleaning, tokenization, and basic NLP metrics.
"""
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Union

logger = logging.getLogger("PitchLens.TextProcessor")

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None


class TextProcessor:
    """Processes document text and computes foundational linguistic metrics."""

    @staticmethod
    def extract_text_from_file(file_path: Union[str, Path]) -> str:
        """
        Extract raw text content from TXT, PDF, or DOCX files.
        Raises ValueError or IOError if format is unsupported or file is corrupted.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".txt":
            return TextProcessor._read_txt(path)
        elif suffix == ".pdf":
            return TextProcessor._read_pdf(path)
        elif suffix in [".docx", ".doc"]:
            return TextProcessor._read_docx(path)
        else:
            raise ValueError(f"Unsupported file format: '{suffix}'. Expected .txt, .pdf, or .docx")

    @staticmethod
    def _read_txt(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1", errors="ignore")

    @staticmethod
    def _read_pdf(path: Path) -> str:
        if pypdf is None:
            raise ImportError("pypdf is required to read PDF files.")
        text_parts = []
        try:
            reader = pypdf.PdfReader(str(path))
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            full_text = "\n".join(text_parts).strip()
            if not full_text:
                raise ValueError("PDF file appears to be empty or contains scanned images without OCR text.")
            return full_text
        except Exception as e:
            logger.error(f"Error reading PDF file {path}: {e}")
            raise ValueError(f"Could not extract text from PDF: {str(e)}")

    @staticmethod
    def _read_docx(path: Path) -> str:
        if docx is None:
            raise ImportError("python-docx is required to read DOCX files.")
        try:
            doc = docx.Document(str(path))
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
            if not full_text:
                raise ValueError("DOCX file contains no readable paragraph text.")
            return full_text
        except Exception as e:
            logger.error(f"Error reading DOCX file {path}: {e}")
            raise ValueError(f"Could not extract text from DOCX: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize raw input text."""
        if not text:
            return ""
        # Replace multiple spaces/newlines with single spaces
        cleaned = re.sub(r"\r\n|\r", "\n", text)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    @staticmethod
    def tokenize_words(text: str, lower: bool = True) -> List[str]:
        """Extract alphanumeric words from text."""
        if lower:
            text = text.lower()
        words = re.findall(r"\b[a-zA-Z0-9$₹%+-]+\b", text)
        return words

    @staticmethod
    def tokenize_sentences(text: str) -> List[str]:
        """Split text into sentences using regex boundary matching."""
        if not text:
            return []
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if s.strip()]

    @classmethod
    def get_basic_metrics(cls, text: str) -> Dict[str, Any]:
        """
        Compute baseline NLP linguistic metrics:
        - word_count
        - sentence_count
        - avg_sentence_length
        - vocabulary_richness (Type-Token Ratio)
        - char_count
        """
        cleaned = cls.clean_text(text)
        words = cls.tokenize_words(cleaned, lower=True)
        sentences = cls.tokenize_sentences(cleaned)

        word_count = len(words)
        sentence_count = len(sentences)
        avg_sent_len = round(word_count / max(sentence_count, 1), 2)
        unique_words = set(words)
        ttr = round(len(unique_words) / max(word_count, 1), 3) if word_count > 0 else 0.0

        return {
            "cleaned_text": cleaned,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sent_len,
            "vocabulary_richness": ttr,
            "unique_word_count": len(unique_words),
            "char_count": len(cleaned),
        }
