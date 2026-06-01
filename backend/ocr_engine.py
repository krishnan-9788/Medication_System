"""
ocr_engine.py - OCR Processing Layer for MedAssist AI
Handles image and PDF text extraction using EasyOCR.
"""

import os
import io
import traceback
from pathlib import Path


def extract_text_from_file(file_path: str) -> dict:
    """
    Extract text from uploaded medical file (image or PDF).
    Returns: dict with 'text', 'success', 'error', 'word_count'
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return {"success": False, "text": "", "error": "File not found", "word_count": 0}

    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return _extract_from_pdf(str(file_path))
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]:
        return _extract_from_image(str(file_path))
    else:
        return {"success": False, "text": "", "error": f"Unsupported file type: {ext}", "word_count": 0}


def _extract_from_image(image_path: str) -> dict:
    """Extract text from image using EasyOCR."""
    try:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        results = reader.readtext(image_path, detail=0, paragraph=True)
        text = "\n".join(results)
        text = _clean_text(text)
        return {
            "success": True,
            "text": text,
            "error": None,
            "word_count": len(text.split())
        }
    except ImportError:
        return {"success": False, "text": "", "error": "EasyOCR not installed. Run: pip install easyocr", "word_count": 0}
    except Exception as e:
        return {"success": False, "text": "", "error": f"OCR failed: {str(e)}", "word_count": 0}


def _extract_from_pdf(pdf_path: str) -> dict:
    """Extract text from PDF - tries text extraction first, then OCR."""
    # First try direct text extraction (for text-based PDFs)
    text = _extract_pdf_text_direct(pdf_path)
    if text and len(text.strip()) > 50:
        text = _clean_text(text)
        return {
            "success": True,
            "text": text,
            "error": None,
            "word_count": len(text.split()),
            "method": "direct_text"
        }

    # If direct extraction fails, convert to image and OCR
    return _extract_pdf_via_ocr(pdf_path)


def _extract_pdf_text_direct(pdf_path: str) -> str:
    """Try to extract text directly from PDF using PyMuPDF or pdfplumber."""
    # Try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        texts = []
        for page in doc:
            texts.append(page.get_text())
        doc.close()
        return "\n".join(texts)
    except ImportError:
        pass
    except Exception:
        pass

    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            texts = []
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    texts.append(t)
        return "\n".join(texts)
    except ImportError:
        pass
    except Exception:
        pass

    return ""


def _extract_pdf_via_ocr(pdf_path: str) -> dict:
    """Convert PDF pages to images and run EasyOCR."""
    try:
        import fitz  # PyMuPDF
        import easyocr
        import numpy as np
        from PIL import Image
        import io

        doc = fitz.open(pdf_path)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        all_text = []

        for page_num in range(min(len(doc), 5)):  # Limit to 5 pages
            page = doc[page_num]
            mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")

            # Convert to numpy array for EasyOCR
            img = Image.open(io.BytesIO(img_bytes))
            img_array = np.array(img)

            results = reader.readtext(img_array, detail=0, paragraph=True)
            all_text.append(f"--- Page {page_num + 1} ---")
            all_text.extend(results)

        doc.close()
        text = _clean_text("\n".join(all_text))
        return {
            "success": True,
            "text": text,
            "error": None,
            "word_count": len(text.split()),
            "method": "pdf_ocr"
        }

    except ImportError as e:
        # Fallback: return empty with helpful message
        return {
            "success": False,
            "text": "",
            "error": f"PDF OCR requires PyMuPDF: pip install PyMuPDF. Error: {str(e)}",
            "word_count": 0
        }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "error": f"PDF OCR failed: {str(e)}",
            "word_count": 0
        }


def _clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    if not text:
        return ""
    # Remove excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    # Remove empty lines (keep single blank lines for readability)
    cleaned = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned.append("")
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    return "\n".join(cleaned).strip()


def validate_file(filename: str, file_size: int, max_size_mb: int = 20) -> dict:
    """Validate uploaded file before processing."""
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    ext = Path(filename).suffix.lower()

    if ext not in allowed_extensions:
        return {
            "valid": False,
            "error": f"File type not allowed. Supported: {', '.join(allowed_extensions)}"
        }

    max_bytes = max_size_mb * 1024 * 1024
    if file_size > max_bytes:
        return {
            "valid": False,
            "error": f"File too large. Maximum size: {max_size_mb}MB"
        }

    return {"valid": True, "error": None}