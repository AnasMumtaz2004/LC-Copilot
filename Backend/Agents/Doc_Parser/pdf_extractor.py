import fitz
from utils.logger import get_logger

logger = get_logger("pdf_extractor")


# Extracting text form pdfs
def extract_text(file_path: str) -> dict:
    result = {
        "text": "",
        "page_count": 0,
        "error": None,
        "file_path": file_path,
    }

    try:
        doc = fitz.open(file_path)
        result["page_count"] = len(doc)
        all_text = []

        for page_num, page in enumerate(doc):
            text = page.get_text()            # Extracting text using normal mode

            if len(text.strip()) < 50:
                logger.debug(f"Page {page_num+1} is empty ,trying block mode")
                text = _extract_blocks(page)

            if text.strip():
                all_text.append(text.strip())
            else:
                logger.warning(f"Page { page_num + 1 } in {file_path} returned no text")
        doc.close()
        result["text"] = "\n\n".join(all_text)

        if not result["text"].strip():
            result["error"] = "no_text_extracted"
            logger.error(f"No text at all from {file_path}")

    except FileNotFoundError:
        result["error"] = "file_not_found"
        logger.error(f"File not found: {file_path}")

    except Exception as e:
        result["error"] = f"extraction_failed: {str(e)}"
        logger.error(f"Failed to extract {file_path}: {e}")

    return result


# Extract text using block mode
def _extract_blocks(page) -> str:
    blocks = page.get_text("blocks")
    lines = []

    for block in blocks:
        if block[6] == 0 and block[4].strip():
            lines.append(block[4].strip())

    return "\n".join(lines)