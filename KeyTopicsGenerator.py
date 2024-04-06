import pdfplumber
import fitz 

import google.generativeai as genai
import os


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text


def summarize_with_gemini(pdf_file_path, model_name='gemini-pro'):
    extracted_text = extract_text_from_pdf(pdf_file_path)

    genai.configure(api_key='***')

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(f'What are the main topics and their subtopics of study of this description so I can prep for this sufficiently? ::: {extracted_text}')

    return response.text


pdf_file_path = '/Users/yetayaltizale/Downloads/2024Syllabus.pdf'
summary = summarize_with_gemini(pdf_file_path)
print(summary) 
