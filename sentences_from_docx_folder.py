import docx
from nltk import sent_tokenize
import csv
import os

def read_docx_and_split_sentences(docx_file_path):
    # Load the DOCX file
    doc = docx.Document(docx_file_path)

    # Extract text from paragraphs
    full_text = ""
    for paragraph in doc.paragraphs:
        full_text += paragraph.text + " "

    # Tokenize text into sentences
    sentences = sent_tokenize(full_text)

    return sentences

def process_docs_in_folder(folder_path, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for filename in os.listdir(folder_path):
            if filename.endswith(".docx"):
                doc_path = os.path.join(folder_path, filename)
                sentences = read_docx_and_split_sentences(doc_path)

                for sentence in sentences:
                    csv_writer.writerow([sentence])

# Replace 'your_folder_path' with the path to your folder containing DOCX files
folder_path = 'path_to_folder'
output_csv_path = 'output_sentences.csv'
process_docs_in_folder(folder_path, output_csv_path)
