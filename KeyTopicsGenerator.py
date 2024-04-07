import pdfplumber
import fitz 

import google.generativeai as genai
import os



class RetrieveTopics:
    def __init__(self) -> None:
        pass

    def extract_text_from_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text


    def summarize_with_gemini(self, pdf_file_path, model_name='gemini-pro'):

        extracted_text = self.extract_text_from_pdf(pdf_file_path)

        genai.configure(api_key='***')

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f'What are the main topics to go over for this subject based on the description so I can prep for this sufficiently?::: {extracted_text}')

        return response.text

    def first_response_verification(self, topics_list):
        return None
        




    def RetrieveTopics(self):
        
        pdf_file_path = '/Users/yetayaltizale/Downloads/CEE 203 S2024 syllabus.pdf'
        summary = self.summarize_with_gemini(pdf_file_path)

        main_topics = summary.split('**')[1:]  # Split by main topics

        topics_list = []
        for i in range(0, len(main_topics), 2):  # Step by 2 to pair titles with their content
            topic_title = main_topics[i].strip()
            if topic_title in ["Main Topics", "Main Topics:", "Subtopics"]:
                continue
            topics_list.append(topic_title)  # Add to the list of main topics

        print(topics_list)
        return topics_list