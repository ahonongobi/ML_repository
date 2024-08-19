import fitz  # PyMuPDF
import os
from sentence_transformers import SentenceTransformer, util

# Initialize the SentenceTransformer model
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

def extract_text_from_pdfs(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text("text") + "\n\n"
            documents.append((filename, text))
    return documents

def preprocess_text(text):
    # Basic text cleaning
    return text.strip().replace('\n', ' ')

def find_relevant_snippets(query, documents):
    query_embedding = model.encode(query, convert_to_tensor=True)
    results = []

    for filename, text in documents:
        paragraphs = text.split('\n\n')  # Split text into paragraphs
        for paragraph in paragraphs:
            paragraph = preprocess_text(paragraph)
            if paragraph:
                paragraph_embedding = model.encode(paragraph, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(query_embedding, paragraph_embedding).item()
                if similarity > 0.2:  # Adjust similarity threshold as needed
                    results.append((filename, paragraph, similarity))

    # Sort results by similarity score and filter out irrelevant snippets
    results = sorted(results, key=lambda x: -x[2])
    filtered_results = []
    for filename, snippet, similarity in results:
        if len(snippet) < 1000:  # Filter out excessively long snippets
            filtered_results.append((filename, snippet, similarity))

    return filtered_results[:3]  # Return top 3 results

# Example usage
folder_path = "../../../Slides"  # Update this path to your folder
query = "What is the main conceptual differences between the Perceptron algorithm and the SVM algorithm?"
documents = extract_text_from_pdfs(folder_path)
results = find_relevant_snippets(query, documents)

# Print the results
for filename, snippet, similarity in results:
    print(f"File: {filename}")
    print(f"Similarity: {similarity:.4f}")
    print(f"Snippet: {snippet[:1000]}...")  # Print only the first 1000 characters of each snippet
    print("=" * 50)
