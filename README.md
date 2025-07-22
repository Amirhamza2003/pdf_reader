# PDF Q&A Chatbot with Groq API

This project provides a Python script that allows you to extract text and images from a PDF, summarize its content, and interactively ask questions about the PDF using the Groq API (Llama 3 model).

## Features

- Extracts text and images from any PDF file
- Simulates image captioning for embedded images
- Summarizes and saves the extracted content as JSON
- Interactive chatbot: ask questions about your PDF and get answers using Groq's Llama 3 model

## Requirements

- Python 3.7 or higher
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [requests](https://docs.python-requests.org/en/latest/)

Install dependencies with:
```bash
pip install pymupdf pillow requests
```

## Setup

1. **Groq API Key:**  
   Get your Groq API key from [Groq](https://console.groq.com/).  
   Replace the value of `GROQ_API_KEY` in the script with your key.

2. **Place your PDF:**  
   Have your PDF file ready. You’ll be prompted for its path when running the script.

## Usage

Run the script:
```bash
python your_script_name.py
```
- Enter the path to your PDF file when prompted.
- The script will extract and summarize the PDF content.
- Ask any question about the PDF in the terminal.
- Type `exit` to quit.

## Output

- Extracted text and simulated image captions are saved in `pdf_summary.json`.
- Answers to your questions are printed in the terminal.

## Notes

- Image captioning is simulated; actual image understanding is not performed.
- The script uses Groq's Llama 3 model for answering questions.

## Troubleshooting

- **ModuleNotFoundError:** Make sure all dependencies are installed.
- **API Errors:** Ensure your Groq API key is correct and has sufficient quota.
- **PDF Extraction Issues:** Some PDFs may have complex layouts that affect extraction quality.

## License

This project is for educational and research purposes only. No warranty is provided.