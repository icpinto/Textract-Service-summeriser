# text_processing.py

from transformers import pipeline

# Load the pre-trained BART model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize the input text
def generate_summary(text, max_length=50, min_length=20):
    if not text.strip():
        raise ValueError("Input text cannot be empty")
    
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

# Function to extract tags from the summarized text
def extract_tags(summary_text):
    words = summary_text.split()
    tags = [word for word in words if len(word) > 3]  # Filtering short words
    return list(set(tags))

# Function to process text and return summary and tags
def process_text(text):
    try:
        summary = generate_summary(text)
        tags = extract_tags(summary)
        return {"summary": summary, "tags": tags}
    except Exception as e:
        raise Exception(f"Error in processing text: {e}")
