import os
import uuid

from .pdf_extractor import extract_text
from .doc_classifier import classify
from .field_extractor import extract_fields_batch
from utils.logger import get_logger

logger = get_logger("doc_parser")

MAX_RETRIES = 2


# Doc Parser node
def doc_parser_node(state):
    run_id = state.get("run_id", str(uuid.uuid4()))
    files = state.get("uploaded_files", [])
    logger.info(f"[{run_id}] starting with {len(files)} files")

    parsed_docs = []
    failed_docs = []

    for file_path in files:
        doc_id = os.path.basename(file_path).replace(" ", "_").lower()
        logger.info(f"processing {doc_id}")

        doc = None
        for attempt in range(MAX_RETRIES):
            try:
                extraction = extract_text(file_path)
                if extraction.get("error"):
                    logger.warning(f"{doc_id} extraction error: {extraction['error']}")
                    continue

                text = extraction.get("text", "")
                if not text.strip():
                    logger.warning(f"{doc_id} empty text")
                    continue

                classification = classify(text, doc_id)
                doc_type = classification.get("doc_type", "unknown")

                if doc_type == "unknown":
                    logger.warning(f"{doc_id} unknown type, retrying")
                    continue

                doc = {
                    "doc_id": doc_id,
                    "doc_type": doc_type,
                    "lc_reference": classification.get("lc_reference"),
                    "confidence": classification.get("confidence"),
                    "raw_text": text,
                    "fields": {}
                }
                break
            except Exception as e:
                logger.error(f"{doc_id} error: {e}")

        if doc:
            parsed_docs.append(doc)
        else:
            failed_docs.append(doc_id)

    if parsed_docs:
       logger.info("running batch field extraction")
       field_results = extract_fields_batch(parsed_docs)

       field_map = {}
       for item in field_results:
        field_map[item["doc_id"]] = item.get("fields", {})

       for d in parsed_docs:
        d["fields"] = field_map.get(d["doc_id"], {})

    lc_reference = None
    for d in parsed_docs:
        fields_lc_ref = d.get("fields", {}).get("lc_reference")
        if fields_lc_ref:
            lc_reference = fields_lc_ref
            break

    return {
        **state,
        "parsed_docs": parsed_docs,
        "failed_docs": failed_docs,
        "lc_reference": lc_reference,
        "current_agent": "doc_parser"
    }