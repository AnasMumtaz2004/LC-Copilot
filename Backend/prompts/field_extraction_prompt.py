SYSTEM_PROMPT = (
    "You are a trade finance document extraction specialist. "
    "Return ONLY valid JSON, no markdown, no explanation."
)

DOCUMENT_SECTION_TEMPLATE = (
    "=== DOCUMENT {index}: {doc_id} ({doc_type}) ===\n"
    "Text:\n{raw_text}\n\n"
    "Fields to extract: {fields_str}\n"
    "Return JSON for this document labeled: DOC_{index}_JSON"
)

CLOSING_INSTRUCTION = (
    "\n\nReturn all documents as a single JSON object with keys "
    "DOC_1_JSON, DOC_2_JSON, etc. If a field is missing use null."
)