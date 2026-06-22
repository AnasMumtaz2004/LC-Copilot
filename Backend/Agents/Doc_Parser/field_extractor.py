import os 
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from graph.state import FIELD_SCHEMA_MAP
from prompts.field_extraction_prompt import (SYSTEM_PROMPT,DOCUMENT_SECTION_TEMPLATE,CLOSING_INSTRUCTION)
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# Creating Full  Prompt 
def create_batch_prompt(documents):
    parts = []
    
    for i, doc in enumerate(documents):
        schema_class = FIELD_SCHEMA_MAP[doc["doc_type"]]
        field_names = list(schema_class.model_fields.keys())
        fields_str = " , ".join(field_names)
        
        section = DOCUMENT_SECTION_TEMPLATE.format(
            index=i + 1,
            doc_id=doc["doc_id"],
            doc_type=doc["doc_type"],
            raw_text=doc["raw_text"][:2000],
            fields_str=fields_str
        )
        parts.append(section)
    
    prompt = "\n\n".join(parts)
    prompt += CLOSING_INSTRUCTION
    return prompt


def extract_fields_batch(documents):
    if not documents:
        return []
    
    valid_docs = []
    for doc in documents:
        if doc["doc_type"] in FIELD_SCHEMA_MAP:
            valid_docs.append(doc)
        else:
            logger.warning(f"Skipping {doc['doc_type']} as no schema exist for it")
        
    if not valid_docs:
        return[]
    
    prompt = create_batch_prompt(valid_docs)
    logger.info(f"sending {len(valid_docs)} docs to groq")
    
    try:
        response = llm.invoke([
            ("system", SYSTEM_PROMPT),
            ("human", prompt)
        ])
        
        raw = response.content.strip()
         
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        batch_result = json.loads(raw)

        results = []
        for i, doc in enumerate(valid_docs):
            doc_id = doc["doc_id"]
            doc_type = doc["doc_type"]
            key = f"DOC_{i+1}_JSON"

            raw_fields = batch_result.get(key, {})
            validated = validate_fields(doc_id, doc_type, raw_fields)

            results.append({
                "doc_id": doc_id,
                "doc_type": doc_type,
                "fields": validated,
                "extraction_error": None
            })

        return results


    except json.JSONDecodeError as e:
        logger.error(f"could not parse json from llm response: {e}")
        results = []
        for d in valid_docs:
            results.append({
                "doc_id": d["doc_id"],
                "doc_type": d["doc_type"],
                "fields": {},
                "extraction_error": "could not parse llm response as json"
            })
        return results

    except Exception as e:
        logger.error(f"batch extraction failed: {e}")
        results = []
        for d in valid_docs:
            results.append({
                "doc_id": d["doc_id"],
                "doc_type": d["doc_type"],
                "fields": {},
                "extraction_error": str(e)
            })
        return results
    
    
def validate_fields(doc_id,doc_type ,raw_fields):
    schema_class = FIELD_SCHEMA_MAP.get(doc_type)
    if not schema_class:
        return raw_fields
    
    try:
        validated = schema_class(**raw_fields)
        return validated.model_dump()
    except Exception as e:
        logger.warning(f"pydantic validation failed for {doc_id} ({doc_type}): {e}")
        return raw_fields


def extract_fields_single(doc_id, doc_type, raw_text):
    result = extract_fields_batch([{"doc_id": doc_id, "doc_type": doc_type, "raw_text": raw_text}])
    if result:
        return result[0]
    return {"doc_id": doc_id,
            "doc_type": doc_type, 
            "fields": {},
            "extraction_error": "single extraction fallback also failed"}