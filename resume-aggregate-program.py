import docx
import os
from glob import glob

print("Resume to Job Matching Program")
print("*******************************")

## If resume in PDF format, you can use pdf2docx library to convert
folder_path = input("Enter path to folder with .docx files: ")
print("-------------------------------------------------------------------------------------------------------------------------------------")

# Create a list of file names
file_list = glob(os.path.join(folder_path, '*.docx'))

# Keyword dictionaries with weights for specific jobs
job_one_keywords = {'Python': 2, 'PHP': 1, 'Admin': 3}
job_two_keywords = {'Javascript': 3, 'Python2': 2, 'Data Science': 7}

# Iterate through all the file names in the list
for file_path in file_list:
    # Open the Word document & remove full path from file_name for readability
    file_name = os.path.basename(file_path)
    doc = docx.Document(file_path)
       
    #Create set to store values found so no repeated strings are add to the value
    found_strings = set()
    found_strings_two = set()
    
    # Initialize a variable to keep track of the total value
    job_one = 0
    job_two = 0
    
    # Iterate through all the paragraphs in the document
    for para in doc.paragraphs:
        # Iterate through all the key strings in the job_one_keywords dictionary
        for key in job_one_keywords:
            # Check if the key string is in the paragraph text
            if key in para.text and key not in found_strings:
                # If the key string is found, add the corresponding value to the total
                job_one += job_one_keywords[key]
                found_strings.add(key)
        # Iterate through all the key strings in the job_two_keywords dictionary
        for key in job_two_keywords:
            # Check if the key string is in the paragraph text
            if key in para.text and key not in found_strings_two:
                # If the key string is found, add the corresponding value to the total and add string to set.
                job_two += job_two_keywords[key]
                found_strings_two.add(key)
    job_one = round(job_one / sum(job_one_keywords.values()) * 100, 2)
    job_two = round(job_two / sum(job_two_keywords.values()) * 100, 2)
    # Print the percentage match for each candidates resume
    print(f"Resume of Candidate '{file_name}' :::: | Job One: {job_one}% match | Job Two: {job_two}% match |")
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    
    
input("Press enter to exit")
