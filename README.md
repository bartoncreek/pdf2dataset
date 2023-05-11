# PDF2Dataset

PDF2Dataset: A robust tool for downloading PDFs, extracting and preprocessing text and metadata with Tika, and creating structured Hugging Face datasets, ready for NLP tasks and embedding creation.

## Features

- Downloads PDFs from provided URLs
- Extracts text and metadata from PDFs using Tika
- Preprocesses text data (tokenization, stopword removal, and punctuation removal)
- Creates Hugging Face datasets from the extracted and preprocessed data
- Saves datasets to disk for easy access and use in future processes

## Installation

``` bash
git clone https://github.com/your_username/pdf2dataset.git
cd pdf2dataset
pip install -r requirements.txt
```

## Usage 

```
from pdf_to_dataset import download_and_extract_text

url = "http://example.com/sample.pdf"
dataset_path = "/path/to/dataset"

dataset = download_and_extract_text(url, dataset_path)
```

## License

This project is licensed under the terms of the MIT license.
