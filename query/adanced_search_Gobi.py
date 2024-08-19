import fitz  # PyMuPDF
import os
import re
import spacy

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")

def extract_key_phrases_spacy(question):
    """
    Use spaCy to extract key phrases from the question.
    """
    doc = nlp(question)
    key_phrases = []

    for chunk in doc.noun_chunks:
        key_phrases.append(chunk.text.lower())

    return key_phrases

def find_best_match(text, key_phrases, definition_patterns):
    """
    Search the text for key phrases and return the surrounding context that matches the definition pattern.
    """
    context_window = 300  # Increase window size for better context

    for key_phrase in key_phrases:
        key_phrase_position = text.lower().find(key_phrase)

        if key_phrase_position != -1:
            # Extract the context around the key phrase
            start_idx = max(key_phrase_position - context_window, 0)
            end_idx = min(key_phrase_position + len(key_phrase) + context_window, len(text))
            context = text[start_idx:end_idx]

            # Look for sentences matching the definition patterns
            for pattern in definition_patterns:
                if re.search(pattern, context, re.IGNORECASE):
                    return context.strip()

    return None

def search_pdfs_for_answer(question, folder_path):
    """
    Search all PDFs in a folder for the answer to a given question.
    """
    results = []
    key_phrases = extract_key_phrases_spacy(question)

    # Patterns that indicate definitions or explanations
    definition_patterns = [
        r"is defined as",
        r"refers to",
        r"means",
        r"is a type of",
        r"is"
    ]

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text()

                # Find the best match for the key phrases in the current page's text
                match = find_best_match(text, key_phrases, definition_patterns)
                if match:
                    results.append((filename, page_num + 1, match))
                    break  # Stop searching the current document once a match is found

    return results

# Example usage
folder_path = "../../../Slides"
question = "What is CNN ?"
results = search_pdfs_for_answer(question, folder_path)

# Print the results
if results:
    for filename, page_num, text in results:
        print(f"Found in {filename}, page {page_num}")
        print(text)
        print("="*50)
else:
    print("No relevant information found.")

#%%

print('heelo')
#%%
















import fitz  # PyMuPDF
import os
import json

def extract_text_from_pdfs(folder_path):
    pdf_texts = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            full_text = ""

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                full_text += text + "\n"

            pdf_texts[filename] = full_text

    return pdf_texts

def save_text_data(text_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(text_data, f)

def load_text_data(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

def query_text_data(query, text_data):
    results = []

    for filename, content in text_data.items():
        if query.lower() in content.lower():
            results.append((filename, content.lower().find(query.lower())))

    return results

# Example usage
folder_path = "../../../Slides"
output_file = "pdf_texts.json"

# Step 1: Extract and save the text from all PDFs
pdf_texts = extract_text_from_pdfs(folder_path)
save_text_data(pdf_texts, output_file)

# Step 2: Load the text data from file
text_data = load_text_data(output_file)

# Step 3: Query the text data
query = "supervised learning"
results = query_text_data(query, text_data)

# Print the results
if results:
    for filename, position in results:
        print(f"Found in {filename} at position {position}")
        start_idx = max(position - 100, 0)
        end_idx = min(position + 500, len(text_data[filename]))
        print(text_data[filename][start_idx:end_idx])
        print("="*50)
else:
    print("No relevant information found.")

#%%
