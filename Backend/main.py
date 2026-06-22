def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()


# main.py

# import os
# import sys

# sys.path.insert(0, os.path.dirname(__file__))

# from Agents.Doc_Parser.pdf_extractor import extract_text

# def run_pdf_tests():
#     base = os.path.dirname(__file__)
#     test_folder = os.path.join(base, "test_data")
    
#     print(f"Looking for: {test_folder}")
#     print(f"Exists: {os.path.exists(test_folder)}\n")
    
#     if not os.path.exists(test_folder):
#         print("Folder not found.")
#         return

#     pdf_files = [f for f in os.listdir(test_folder) if f.endswith(".pdf")]
#     print(f"Found {len(pdf_files)} PDFs\n")

#     for file_name in pdf_files:
#         file_path = os.path.join(test_folder, file_name)
#         print("=" * 60)
#         print(f"Testing: {file_name}")
#         result = extract_text(file_path)

#         if result["error"]:
#             print(f" Error: {result['error']}")
#         else:
#             print(f"Pages: {result['page_count']} | Chars: {len(result['text'])}")
#             print(result["text"])
#             print()

# if __name__ == "__main__":
#     run_pdf_tests()\
    
    

# import os
# import sys

# sys.path.insert(0, os.path.dirname(__file__))

# from Agents.Doc_Parser.pdf_extractor import extract_text
# from Agents.Doc_Parser.doc_classifier import classify
# from Agents.Doc_Parser.field_extractor import extract_fields_batch

# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


# def main():
#     print("Hello from backend!\n")

#     if not os.path.exists(TEST_DATA_DIR):
#         print(f"Test data folder not found: {TEST_DATA_DIR}")
#         return

#     pdf_files = sorted([f for f in os.listdir(TEST_DATA_DIR) if f.endswith(".pdf")])

#     if not pdf_files:
#         print("No PDF files found in test_data folder.")
#         return

#     print(f"Found {len(pdf_files)} PDFs\n")
#     print("=" * 60)

#     extracted_docs = []

#     # Step 1: PDF text extraction
#     # Step 2: Document classification
#     for filename in pdf_files:
#         file_path = os.path.join(TEST_DATA_DIR, filename)

#         extracted = extract_text(file_path)

#         if extracted["error"]:
#             print(f"[FAILED] {filename} -> {extracted['error']}\n")
#             continue

#         # make doc_id from filename since extractor currently doesn't return doc_id
#         doc_id = os.path.splitext(filename)[0]

#         # extractor returns "text", not "raw_text"
#         raw_text = extracted["text"]

#         # classifier function name is classify(), not classify_document()
#         classification = classify.invoke({
#             "text": raw_text,
#             "doc_id": doc_id
#         })

#         print(f"File       : {filename}")
#         print(f"Pages      : {extracted['page_count']}")
#         print(f"Doc type   : {classification['doc_type']}")
#         print(f"Confidence : {classification['confidence']}")
#         print(f"LC Ref     : {classification['lc_reference']}")

#         top3 = sorted(
#             classification["scores"].items(),
#             key=lambda x: x[1],
#             reverse=True
#         )[:3]
#         print(f"Top scores : {top3}")
#         print()

#         extracted_docs.append({
#             "doc_id": doc_id,
#             "doc_type": classification["doc_type"],
#             "raw_text": raw_text
#         })

#     # Step 3: Field extraction
#     print("=" * 60)
#     print(f"Running field extraction on {len(extracted_docs)} docs...\n")

#     field_results = extract_fields_batch(extracted_docs)

#     for r in field_results:
#         print(f"Doc ID    : {r['doc_id']}")
#         print(f"Doc type  : {r['doc_type']}")
#         print(f"Error     : {r.get('extraction_error')}")
#         print(f"Fields    : {r['fields']}")
#         print()


# if __name__ == "__main__":
#     main()



import os
import sys
from pprint import pprint

sys.path.insert(0, os.path.dirname(__file__))

from Agents.Doc_Parser.doc_parser import doc_parser_node

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_transaction_pdfs")


def main():
    print("Testing Agent 1...\n")

    if not os.path.exists(TEST_DATA_DIR):
        print("test_data folder not found")
        return

    pdf_files = sorted([
        os.path.join(TEST_DATA_DIR, f)
        for f in os.listdir(TEST_DATA_DIR)
        if f.lower().endswith(".pdf")
    ])

    if not pdf_files:
        print("No PDFs found in test_data")
        return

    print(f"Found {len(pdf_files)} PDFs")
    for f in pdf_files:
        print("-", os.path.basename(f))

    state = {
        "uploaded_files": pdf_files
    }

    print("\nRunning doc_parser_node...\n")
    result = doc_parser_node(state)

    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)
    print(f"LC Reference: {result.get('lc_reference')}")
    print(f"Failed docs : {result.get('failed_docs')}")
    print()

    for doc in result.get("parsed_docs", []):
        print("=" * 80)
        print(f"Doc ID     : {doc.get('doc_id')}")
        print(f"Doc Type   : {doc.get('doc_type')}")
        print(f"Confidence : {doc.get('confidence')}")
        print(f"LC Ref     : {doc.get('lc_reference')}")
        print("Fields:")
        pprint(doc.get("fields", {}))
        print()

if __name__ == "__main__":
    main()