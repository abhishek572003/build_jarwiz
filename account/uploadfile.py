
from .forms import *
from .models import *
import os
from django.core.files.storage import FileSystemStorage
import datetime
from subplatform.settings import *
from .ocr_jarwiz_final import *
import PyPDF2
import shutil
from pdf2image import convert_from_path


def uploadfiles(fname, username, inpfile, path):
    ts=datetime.datetime.now()
    splitName = fname.split('.')
    numberOfParts = len(splitName)
    ext = splitName[numberOfParts-1] 
    filename = username+str(ts)+"."+ext
    filename = filename.replace("-","")
    filename = filename.replace(":","")
    filename = filename.replace(" ","")
    fs=FileSystemStorage(location=path)
    file_ins = fs.save(filename, inpfile)
    file_url = os.path.join(path, filename)
    fileData = {'fname':fname,'newname':filename,'ext':ext,'file_url':file_url}
    tags=""
    if ext=='png' or ext=='jpeg' or ext=='jpg' or ext=='webp' or ext=='heic' or ext=='heif':
        tags = classify_model(file_url)   
    elif ext=='pdf':
        isencrypted = check_pdf_encryption(file_url)
        if not isencrypted:
            temppath=os.path.join(path,'temp')
            os.mkdir(temppath)
            pages = convert_from_path(file_url, 500, output_folder=temppath, first_page=1, last_page=1, poppler_path='/usr/bin')
            for page in pages:
                page.save(temppath+"/first.jpg", 'JPEG')
            tags = classify_model(temppath+"/first.jpg")
            shutil.rmtree(temppath)
        else:
            tags="encryptedfile"
    else:
        tags="unreadablefiletype"
    info = [tags, filename, file_url, ext]
    return info


def classify_model(image_path):
    user_prompt="Extract the title of the file and Classify the file as one of the following: Tickets, Hotel vouchers, Legal agreements, Bank statements, Expense vouchers, Medical report, Warranty, Identity Document. And the give output as Title: and Classification."
    system_prompt="""You are specialist in comprehending documents. Input files and comprehend amd classify them as tickets,hotel vouchers,legal agreements,bank statements,
                    expense vouchers,medical reports, invoices, warranty,identity documents. Extract data of the document in the form of json format and give an output."""
    output= gemini_output(image_path, system_prompt, user_prompt)
    print(output)
    final_op=""
    if "ticket" in output or "Ticket" in output:
        user_prompt="Extract the date, source, destination, departure time and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "Hotel voucher" in output or "hotel voucher" in output:
        user_prompt="Extract the name, checkin time and date and checkout time and date and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "legal" in output or "Legal" in output:
        user_prompt="Extract the name of parties, date of signing, title of document and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "bank" in output or "Bank" in output:
        user_prompt="Extract the name of customer, name of bank, account number and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "expense" in output or "Expense" in output:
        user_prompt="Extract the title as the receiver, date and invoice number or bill number and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "medical" in output or "Medical" in output:
        user_prompt="Extract the name of patient, diagnostic test names and date and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "warranty" in output or "Warranty" in output:
        user_prompt="Extract the type of machine, comapny name, date of issue and date of expiry and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    elif "identity" in output or "Identity" in output:
        user_prompt="Extract the title as type of identity document and name on document and give reponse as data separated by commas"
        final_op = gemini_output(image_path, system_prompt, user_prompt)
        print(final_op)
    return final_op

def check_pdf_encryption(file):
    # Open the PDF file
    with open(file, 'rb') as pdf_file:
        # Create a PdfFileReader object
        pdf_reader = PyPDF2.PdfReader(open(file, 'rb'))
        # Check if the PDF is encrypted
        if pdf_reader.is_encrypted:
            return True
        else:
            return False
