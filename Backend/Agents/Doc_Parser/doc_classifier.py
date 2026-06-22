import re
from utils.logger import get_logger

logger = get_logger("doc_classifier")

# Keywords  to match
KEYWORD_WEIGHTS = {
    "lc_terms": {
        "letter of credit": 5,
        "documentary credit": 5,
        "irrevocable": 4,
        "issuing bank": 4,
        "applicant": 3,
        "beneficiary": 3,
        "expiry date": 3,
        "mt700": 4,
        "swift": 2,
        "advising bank": 3,
        "presentation": 2,
        "documents required": 3,
        "partial shipment": 2,
        "transhipment": 2,
        "ucp 600": 3,
    },
    "invoice": {
        "commercial invoice": 6,
        "invoice no": 4,
        "invoice number": 4,
        "invoice date": 3,
        "seller": 3,
        "buyer": 3,
        "unit price": 4,
        "total amount": 3,
        "amount due": 3,
        "goods description": 2,
        "pro forma": 2,
        "payment terms": 2,
        "incoterms": 2,
    },
    "bill_of_lading": {
        "bill of lading": 6,
        "b/l": 4,
        "bl number": 4,
        "shipped on board": 5,
        "shipper": 3,
        "consignee": 3,
        "notify party": 3,
        "vessel": 3,
        "port of loading": 3,
        "port of discharge": 3,
        "freight": 3,
        "master": 2,
        "carrier": 3,
        "on board date": 4,
        "clean on board": 4,
    },
    "packing_list": {
        "packing list": 6,
        "packing no": 4,
        "gross weight": 4,
        "net weight": 4,
        "carton": 3,
        "package": 3,
        "number of packages": 4,
        "cbm": 3,
        "dimensions": 2,
        "pallets": 2,
        "ctn": 3,
    },
    "certificate_of_origin": {
        "certificate of origin": 6,
        "country of origin": 5,
        "origin certificate": 4,
        "chamber of commerce": 4,
        "manufactured in": 3,
        "produced in": 3,
        "exporter": 3,
        "consignee": 2,
        "certify": 3,
    },
    "insurance_certificate": {
        "insurance certificate": 6,
        "insurance policy": 5,
        "certificate of insurance": 5,
        "insured": 4,
        "all risks": 4,
        "premium": 3,
        "coverage": 3,
        "underwriter": 3,
        "claim": 2,
        "institute cargo clauses": 4,
        "war risk": 3,
    },
    "draft": {
        "bill of exchange": 6,
        "draft": 4,
        "at sight": 5,
        "pay to the order": 5,
        "drawee": 4,
        "drawer": 4,
        "tenor": 4,
        "days after sight": 4,
        "exchange for": 3,
        "value received": 3,
    },
    "inspection_certificate": {
        "inspection certificate": 6,
        "certificate of inspection": 5,
        "inspected by": 4,
        "inspection report": 4,
        "quality": 3,
        "quantity": 2,
        "inspector": 4,
        "surveyor": 3,
        "complies with": 3,
        "specification": 2,
        "third party inspection": 4,
        "sgs": 3,
        "bureau veritas": 3,
        "intertek": 3,
    },
}

LC_REF_PATTERNS = [
    r"LC[\/\-\s]?[A-Z0-9]*\d[A-Z0-9\-\/]{2,20}",
    r"L\.?C\.?\s*(?:No|Reference|Ref)\.?\s*:?\s*([A-Z0-9][A-Z0-9\-\/]*\d[A-Z0-9\-\/]*)",
    r"Credit\s+No\.?\s*:?\s*([A-Z0-9][A-Z0-9\-\/]*\d[A-Z0-9\-\/]*)",
    r"Documentary\s+Credit\s+No\.?\s*:?\s*([A-Z0-9][A-Z0-9\-\/]*\d[A-Z0-9\-\/]*)",
    r"\b[A-Z]{2,6}-?\d{4,}-[A-Z0-9\-]{2,20}\b",
    r"Ref\.?\s*No\.?\s*:?\s*([A-Z0-9][A-Z0-9\-\/]*\d[A-Z0-9\-\/]*)",
]


def classify(text, doc_id=""):
    """Classify LC document type using keyword scoring."""
    if not text or not text.strip():
        logger.warning(f"Empty text passed for doc {doc_id}")
        return {"doc_type": "unknown", "confidence": "low", "lc_reference": None, "scores": {}}

    text_lower = text.lower()
    scores = {}

    for doc_type, keywords in KEYWORD_WEIGHTS.items():
        total = 0
        for keyword, weight in keywords.items():
            if keyword in text_lower:
                total += weight
        scores[doc_type] = total

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_type, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0

    if best_score == 0:
        logger.warning(f"No keywords matched at all for {doc_id}")
        return {"doc_type": "unknown", "confidence": "low", "lc_reference": None, "scores": scores}

    gap = best_score - second_score
    if gap >= 4:
        confidence = "high"
    elif gap >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    # try to extract the LC reference number from text
    lc_ref = None
    for pattern in LC_REF_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_match = match.group(1) if match.lastindex else match.group(0)
            lc_ref = re.sub(r'\s+', ' ', raw_match.strip())
            break

    logger.debug(f"{doc_id}: {best_type} (score={best_score}, gap={gap}, confidence={confidence})")

    return {
        "doc_type": best_type,
        "confidence": confidence,
        "lc_reference": lc_ref,
        "scores": scores,
    }