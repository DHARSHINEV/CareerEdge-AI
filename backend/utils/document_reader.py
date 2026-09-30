"""
CareerEdge AI - Local Document Reader & Extractor
Safely extracts text from PDF, DOCX, and TXT files without external network calls.
Handles corrupted files, scan warnings, and enforces size constraints.
"""

import os
import io
import re
import logging
from typing import Tuple
from pypdf import PdfReader
from docx import Document

logger = logging.getLogger("careeredge.docreader")

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit


class DocumentReader:
    """
    Local document parser supporting PDF, DOCX, and TXT formats.
    """

    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> Tuple[str, str]:
        """
        Extracts clean plain text from bytes based on file extension.
        Returns: (extracted_text, document_type)
        """
        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds maximum permitted limit ({MAX_FILE_SIZE_BYTES // (1024*1024)}MB)")

        ext = os.path.splitext(filename.lower())[1]

        if ext == ".pdf":
            return DocumentReader._read_pdf(file_bytes), "PDF"
        elif ext in [".docx", ".doc"]:
            return DocumentReader._read_docx(file_bytes), "DOCX"
        elif ext in [".txt", ".md"]:
            return DocumentReader._read_txt(file_bytes), "TXT"
        else:
            raise ValueError(f"Unsupported file format '{ext}'. Supported formats: .pdf, .docx, .txt")

    @staticmethod
    def _read_pdf(file_bytes: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)

            full_text = "\n\n".join(text_parts).strip()
            if not full_text:
                raise ValueError("PDF contains no selectable text. It may be a scanned image or empty.")
            return full_text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def _read_docx(file_bytes: bytes) -> str:
        try:
            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                    if row_text:
                        paragraphs.append(row_text)

            full_text = "\n\n".join(paragraphs).strip()
            if not full_text:
                raise ValueError("DOCX document contains no text.")
            return full_text
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

    @staticmethod
    def _read_txt(file_bytes: bytes) -> str:
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                return file_bytes.decode(enc).strip()
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode plain text file with standard encodings.")
