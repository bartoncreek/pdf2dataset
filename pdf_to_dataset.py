import os
import urllib.request
from urllib.error import URLError
from tika import parser
from datasets import Dataset
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def download_and_extract_text(url, dataset):
    """
    Downloads a PDF from a URL, extracts its text and metadata using Tika,
    preprocesses the text, and adds the data to a Hugging Face Dataset.

    Args:
    url (str): The URL of the PDF to download and extract data from.
    dataset (str): The directory to save the Hugging Face Dataset in.

    Returns:
    Dataset: The Hugging Face Dataset containing the extracted and preprocessed text and metadata.
    """
    # Verify URL
    try:
        response = urllib.request.urlopen(url)
    except URLError as e:
        print(f'Invalid URL. Error: {e.reason}')
        return None

    # Check if dataset directory exists
    if not os.path.exists(dataset):
        print(f'Dataset directory does not exist: {dataset}')
        return None

    # Check if file is already downloaded
    filename = url.split("/")[-1]
    if not os.path.isfile(filename):
        # Download the file
        urllib.request.urlretrieve(url, filename)

    # Set environment variable for UTF-8 encoding
    os.environ["PYTHONIOENCODING"] = "utf8"

    # Extract text and metadata using Tika
    parsed = parser.from_file(filename, xmlContent=False)
    
    # Preprocess the text
    # Convert to lowercase
    text = parsed['content'].lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize and remove stopwords
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    # Prepare metadata
    metadata = parsed['metadata']

    # Check if dataset already exists
    if os.path.isfile(dataset + '/dataset.arrow'):
        # Load the existing dataset
        hf_dataset = Dataset.load_from_disk(dataset)
        # Add the new data to it
        hf_dataset = hf_dataset.add_item({
            'content': tokens_without_sw,
            'metadata': [metadata]
        })
    else:
        # Create a new Hugging Face dataset
        hf_dataset = Dataset.from_dict({
            'content': [tokens_without_sw],
            'metadata': [metadata]
        })

    # Save the dataset to disk
    hf_dataset.save_to_disk(dataset)

    # Report basic dataset info
    print("Dataset Info:")
    print("Number of rows: ", hf_dataset.num_rows)
    print("Number of columns: ", hf_dataset.num_columns)
    print("Column names: ", hf_dataset.column_names)
    print("Shape: ", hf_dataset.shape)

    return hf_dataset
