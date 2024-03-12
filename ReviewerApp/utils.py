from PyPDF2 import PdfReader
from openai import OpenAI
from spire.doc import *
from spire.doc.common import *
import os
import dotenv

dotenv.load_dotenv()

def extract_text(file_path) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """
    print("Text Extraction started!!")
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() + '\n'
        print("Text Extracted!!")
        return text


def save_file(file_path, file):
    """
    Save the given file to the specified file path.

    Args:
        file_path (str): The path where the file should be saved.
        file (File): The file object to be saved.

    Returns:
        None
    """
    print("File saving started!!")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print("File saved locally!!")


def convert_doc_to_pdf(file_path):
    """
    Converts a Microsoft Word document (.docx) to a PDF file.

    Args:
        file_path (str): The path to the .docx file.

    Returns:
        str: The path to the converted PDF file.
    """
    print("Converting to PDF started!!")
    doc = Document()
    doc.LoadFromFile(file_path)
    pdf_path = file_path.replace('.docx', '.pdf')
    doc.SaveToFile(pdf_path, FileFormat.PDF)
    doc.Close()
    print("Converted to PDF!!")
    return pdf_path


def get_feedback(text: str) -> str:
    """
    Generates feedback on a given resume text.

    Args:
        text (str): The resume text to generate feedback on.

    Returns:
        str: The generated feedback.

    Raises:
        None
    """
    prompt = "Assume that you are an HR and looking to hire a Software Development Engineer so, please provide feedback on the resume and if you feel that the data given to you is wrong and doesn't associate or looks like a resume, then just return 'Incorrect Data' only and nothing else with the data, only return 'Incorrect Data'" + text
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1975,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print("Feedback generated!!")
    return response.choices[0].message.content