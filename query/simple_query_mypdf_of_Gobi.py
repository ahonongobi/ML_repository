import fitz  # PyMuPDF
import os
import re

def search_pdfs(query, folder_path):
    results = []
    query = query.lower()
    query_tokens = query.split()

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_lower = text.lower()

                # Check for multi-word query (exact phrase match)
                if " ".join(query_tokens) in text_lower:
                    results.append((filename, page_num + 1, text))
                # Check if all query words are present in text
                elif all(token in text_lower for token in query_tokens):
                    results.append((filename, page_num + 1, text))

    # Rank results by relevance (simple ranking based on frequency of query terms)
    ranked_results = sorted(results, key=lambda x: sum(x[2].lower().count(token) for token in query_tokens), reverse=True)

    return ranked_results

# Example usage
folder_path = "../../../Slides"
query = "learning"
results = search_pdfs(query, folder_path)

# Print the results with highlighted matches
for filename, page_num, text in results:
    highlighted_text = re.sub(f"(?i)({re.escape(query)})", r"\033[44;33m\1\033[m", text)
    print(f"Found in {filename}, page {page_num}")
    print(highlighted_text)
    print("="*50)

#%%

#%%

#%%
