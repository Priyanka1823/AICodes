import re
import pandas as pd

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize into sentences by splitting on periods
    sentences = text.split('.')
    # Remove any extra whitespace and empty strings
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def levenshtein_distance_table(s1, s2):
    """Generate and print the Levenshtein distance table."""
    rows = len(s1) + 1
    cols = len(s2) + 1
    dist_table = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialize first row and column
    for i in range(1, rows):
        dist_table[i][0] = i  # Deletions to convert s1[:i] to empty string
    for j in range(1, cols):
        dist_table[0][j] = j  # Insertions to convert empty string to s2[:j]

    # Fill the table with Levenshtein distances
    for i in range(1, rows):
        for j in range(1, cols):
            if s1[i - 1] == s2[j - 1]:
                dist_table[i][j] = dist_table[i - 1][j - 1]  # No cost for matching characters
            else:
                dist_table[i][j] = min(
                    dist_table[i - 1][j] + 1,   # Deletion
                    dist_table[i][j - 1] + 1,   # Insertion
                    dist_table[i - 1][j - 1] + 1  # Substitution
                )
    
    # Create a DataFrame for a clean, tabular output
    df = pd.DataFrame(dist_table, 
                      index=[" "] + list(s1), 
                      columns=[" "] + list(s2))
    print("\nEdit Distance Table:")
    print(df.to_string())  # Print the table as a formatted string
    
    return dist_table[-1][-1]  # Return the final edit distance

def detect_plagiarism(doc1, doc2, threshold=5):
    doc1_sentences = preprocess_text(doc1)
    doc2_sentences = preprocess_text(doc2)
    alignments = []

    print(f"\nDocument 1 Sentences: {doc1_sentences}")
    print(f"Document 2 Sentences: {doc2_sentences}\n")

    for i in range(len(doc1_sentences)):
        for j in range(len(doc2_sentences)):
            print(f"\nComparing:\n'{doc1_sentences[i]}'\nwith\n'{doc2_sentences[j]}'")
            dist = levenshtein_distance_table(doc1_sentences[i], doc2_sentences[j])
            print(f"Edit Distance: {dist}")
            if dist <= threshold:
                alignments.append((doc1_sentences[i], doc2_sentences[j], dist))

    if not alignments:
        print("\nNo plagiarism detected.")
    else:
        print(f"\nPlagiarism detected with threshold {threshold}.\n")

    return alignments


doc1 = input("Enter the text for Document 1: ").strip()
doc2 = input("Enter the text for Document 2: ").strip()

# Ensure non-empty inputs
if not doc1 or not doc2:
    raise ValueError("Both documents must contain text.")

try:
    threshold = int(input("Enter the threshold value for plagiarism detection: ").strip())
except ValueError:
    raise ValueError("Threshold must be an integer.")

# Run plagiarism detection
plagiarism_results = detect_plagiarism(doc1, doc2, threshold)

for sent1, sent2, dist in plagiarism_results:
    print(f"Potential plagiarism detected:\nDoc1: {sent1}\nDoc2: {sent2}\nEdit Distance: {dist}\n")
