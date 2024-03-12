from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.conf import settings
from .utils import extract_text, save_file, get_feedback, convert_doc_to_pdf
import os


@api_view(['POST'])
def feedback_on_resume(request):
    """
    Extracts text from the uploaded resume file, generates feedback on the resume text,
    and returns the feedback as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing the feedback message.

    Raises:
        KeyError: If the 'resume' file is not found in the request.FILES dictionary.
    """
    file = request.FILES['resume']
    files_to_delete = []
    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    save_file(file_path, file)

    files_to_delete.append(file_path)

    if file_path.endswith('.docx'):
        file_path = convert_doc_to_pdf(file_path)
        files_to_delete.append(file_path)

    text = extract_text(file_path)
    feedback = get_feedback(text)

    for files in files_to_delete:
        os.remove(files)

    if "Incorrect Data" in feedback:
        return Response({'message': "Uploaded data is not a Resume!!"}, status=HTTP_400_BAD_REQUEST)
    return Response({'message': feedback}, status=HTTP_200_OK)

