# from flask import Flask, request, jsonify
# import fitz  # PyMuPDF
# import spacy
# from spacy.pipeline import EntityRuler
# import urllib.parse
# import os
# import re

# app = Flask(__name__)

# # Load the pretrained model
# nlp = spacy.load("en_core_web_lg")

# # Define the path to the patterns file
# skills_pattern_file = "jz_skill_patterns.jsonl"

# # Create an EntityRuler instance with a unique name
# ruler = nlp.add_pipe("entity_ruler", name="my_entity_ruler")

# # Load patterns from disk
# ruler.from_disk(skills_pattern_file)

# # Regular expression pattern for matching email addresses
# email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# # Regular expression pattern for matching phone numbers (supports various formats)
# phone_pattern = r'\b(?:\+\d{1,2}\s*)?(?:(?:\d{1,3}[\s.-]*)?\d{3}[\s.-]*\d{3}[\s.-]*\d{4})\b'


# @app.route('/spacy_extract_skills', methods=['POST'])
# def extract_skills():
#     print("Received request")
#     if not request.is_json:
#         print("Request is not JSON")
#         return jsonify({"error": "Request content type must be application/json"}), 415

#     try:
#         # Receive file URL from the request
#         file_url = request.json.get('file_url')
#         print("File URL:", file_url)
#         if file_url:
#             # Convert file URI to local file path
#             file_path = urllib.parse.urlparse(file_url).path
#             print("File path from URL:", file_path)
#             # Decode URL-encoded characters in the file path
#             file_path = urllib.parse.unquote(file_path)
#             print("Decoded file path:", file_path)
            
#             # Check if the file path is a UNC path
#             if file_path.startswith("\\\\"):
#                 # Use the UNC path directly
#                 network_path = file_path
#             else:
#                 # Assume the file is on another network and construct the UNC path accordingly
#                 network_path = "\\\\" + file_path.replace('/', '\\')
#             print("Network path:", network_path)
            
#             # Verify the existence of the file
#             if not os.path.exists(network_path):
#                 return jsonify({"error": f"No such file: '{network_path}'"}), 404
            
#             # Extract text from PDF
#             text = ""
#             with fitz.open(network_path) as pdf_doc:
#                 for page in pdf_doc:
#                     text += page.get_text()

#             # Check if "dotnet" or ".net" is present in the text
#             dotnet_present = "dotnet" in text.lower()
#             dot_net_present = ".net" in text.lower()
#             java_present = "java" in text.lower()

#             # Process text to extract skills 
#             doc = nlp(text)
#             skills = set()
#             for ent in doc.ents:
#                 if ent.label_ == 'SKILL':
#                     skills.add(ent.text.lower().capitalize())

#             # Include "dotnet" and ".net" in the extracted skills if present
#             if dotnet_present:
#                 skills.add("Dotnet")
#             if dot_net_present:
#                 skills.add(".Net")
#             if java_present:
#                 skills.add("Java")

#             # Extract email addresses and phone numbers using regular expressions
#             emails = re.findall(email_pattern, text)
#             phones = re.findall(phone_pattern, text)

#             print("Skills extracted:", skills)
#             print("Emails extracted:", emails)
#             print("Phone numbers extracted:", phones)

#             return jsonify({"skills": list(skills), "emails": emails, "phones": phones})
#         else:
#             print("No file URL received")
#             return jsonify({"error": "No file URL received."}), 400
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)



# local and network

from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import spacy
from spacy.pipeline import EntityRuler
import urllib.parse
import os
import re

app = Flask(__name__)
import spacy.cli
spacy.cli.download("en_core_web_lg")

# Load the pretrained model
nlp = spacy.load("en_core_web_lg")

# Define the path to the patterns file
skills_pattern_file = "jz_skill_patterns.jsonl"

# Create an EntityRuler instance with a unique name
ruler = nlp.add_pipe("entity_ruler", name="my_entity_ruler")

# Load patterns from disk
ruler.from_disk(skills_pattern_file)

# Regular expression pattern for matching email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Regular expression pattern for matching phone numbers (supports various formats)
phone_pattern = r'\b(?:\+\d{1,2}\s*)?(?:(?:\d{1,3}[\s.-]*)?\d{3}[\s.-]*\d{3}[\s.-]*\d{4})\b'


@app.route('/spacy_extract_skills', methods=['POST'])
def extract_skills():
    print("Received request")
    if not request.is_json:
        print("Request is not JSON")
        return jsonify({"error": "Request content type must be application/json"}), 415

    try:
        # Receive file URL from the request
        file_url = request.json.get('file_url')
        print("File URL:", file_url)
        if file_url:
            # Convert file URI to local file path
            file_path = urllib.parse.urlparse(file_url).path
            print("File path from URL:", file_path)
            # Decode URL-encoded characters in the file path
            file_path = urllib.parse.unquote(file_path)
            print("Decoded file path:", file_path)
            
            # Check if the file path is a UNC path
            if file_path.startswith("\\\\"):
                # Use the UNC path directly
                network_path = file_path
            else:
                # Assume the file is on another network and construct the UNC path accordingly
                network_path = "\\\\" + file_path.replace('/', '\\')
                print("Network path:", network_path)
                
                # Verify the existence of the file in the network path
                if os.path.exists(network_path):
                    # Extract text from PDF
                    text = ""
                    with fitz.open(network_path) as pdf_doc:
                        for page in pdf_doc:
                            text += page.get_text()

                    # Check if "dotnet" or ".net" is present in the text
                    dotnet_present = "dotnet" in text.lower()
                    dot_net_present = ".net" in text.lower()
                    java_present = "java" in text.lower()

                    # Process text to extract skills 
                    doc = nlp(text)
                    skills = set()
                    for ent in doc.ents:
                        if ent.label_ == 'SKILL':
                            skills.add(ent.text.lower().capitalize())

                    # Include "dotnet" and ".net" in the extracted skills if present
                    if dotnet_present:
                        skills.add("Dotnet")
                    if dot_net_present:
                        skills.add(".Net")
                    if java_present:
                        skills.add("Java")

                    # Extract email addresses and phone numbers using regular expressions
                    emails = re.findall(email_pattern, text)
                    phones = re.findall(phone_pattern, text)

                    print("Skills extracted:", skills)
                    print("Emails extracted:", emails)
                    print("Phone numbers extracted:", phones)

                    return jsonify({"skills": list(skills), "emails": emails, "phones": phones})

            # If the file is not found in the network path, check in the local path
            local_path = file_path.replace("\\", "/")
            print("Local path:", local_path)

            # Verify the existence of the file in the local path
            if os.path.exists(local_path):
                # Extract text from PDF
                text = ""
                with fitz.open(local_path) as pdf_doc:
                    for page in pdf_doc:
                        text += page.get_text()

                # Check if "dotnet" or ".net" is present in the text
                dotnet_present = "dotnet" in text.lower()
                dot_net_present = ".net" in text.lower()
                java_present = "java" in text.lower()

                # Process text to extract skills 
                doc = nlp(text)
                skills = set()
                for ent in doc.ents:
                    if ent.label_ == 'SKILL':
                        skills.add(ent.text.lower().capitalize())

                # Include "dotnet" and ".net" in the extracted skills if present
                if dotnet_present:
                    skills.add("Dotnet")
                if dot_net_present:
                    skills.add(".Net")
                if java_present:
                    skills.add("Java")

                # Extract email addresses and phone numbers using regular expressions
                emails = re.findall(email_pattern, text)
                phones = re.findall(phone_pattern, text)

                print("Skills extracted:", skills)
                print("Emails extracted:", emails)
                print("Phone numbers extracted:", phones)

                return jsonify({"skills": list(skills), "emails": emails, "phones": phones})

            # If the file is not found in the local path as well
            print("File not found in local path.")
            return jsonify({"error": f"No such file: '{local_path}'"}), 404

        else:
            print("No file URL received")
            return jsonify({"error": "No file URL received."}), 400

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
   













# from flask import Flask, request, jsonify
# import fitz  # PyMuPDF
# import spacy
# from spacy.pipeline import EntityRuler
# import urllib.parse
# import os

# app = Flask(__name__)

# # Load the pretrained model
# nlp = spacy.load("en_core_web_lg")

# # Define the path to the patterns file
# skills_pattern_file = "jz_skill_patterns.jsonl"

# # Create an EntityRuler instance with a unique name
# ruler = nlp.add_pipe("entity_ruler", name="my_entity_ruler")

# # Load patterns from disk
# ruler.from_disk(skills_pattern_file)

# @app.route('/spacy_extract_skills', methods=['POST'])
# def extract_skills():
#     print("Received request")
#     if not request.is_json:
#         print("Request is not JSON")
#         return jsonify({"error": "Request content type must be application/json"}), 415

#     try:
#         # Receive file URL from the request
#         file_url = request.json.get('file_url')
#         print("File URL:", file_url)
#         if file_url:
#             # Convert file URI to local file path
#             file_path = urllib.parse.urlparse(file_url).path
#             print("File path from URL:", file_path)
#             # Decode URL-encoded characters in the file path
#             file_path = urllib.parse.unquote(file_path)
#             print("Decoded file path:", file_path)
            
#             # Check if the file path is a UNC path
#             if file_path.startswith("\\\\"):
#                 # Use the UNC path directly
#                 network_path = file_path
#             else:
#                 # Assume the file is on another network and construct the UNC path accordingly
#                 network_path = "\\\\" + file_path.replace('/', '\\')
#             print("Network path:", network_path)
            
#             # Verify the existence of the file
#             if not os.path.exists(network_path):
#                 return jsonify({"error": f"No such file: '{network_path}'"}), 404
            
#             # Extract text from PDF
#             text = ""
#             with fitz.open(network_path) as pdf_doc:
#                 for page in pdf_doc:
#                     text += page.get_text()

#             # Check if "dotnet" or ".net" is present in the text
#             dotnet_present = "dotnet" in text.lower()
#             dot_net_present = ".net" in text.lower()
#             java_present = "java" in text.lower()

#             # Process text to extract skills 
#             doc = nlp(text)
#             skills = set()
#             for ent in doc.ents:
#                 if ent.label_ == 'SKILL':
#                     skills.add(ent.text.lower().capitalize())

#             # Include "dotnet" and ".net" in the extracted skills if present
#             if dotnet_present:
#                 skills.add("Dotnet")
#             if dot_net_present:
#                 skills.add(".Net")
#             if java_present:
#                 skills.add("Java")

#             print("Skills extracted:", skills)
#             return jsonify({"skills": list(skills)})
#         else:
#             print("No file URL received")
#             return jsonify({"error": "No file URL received."}), 400
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':

#     app.run(debug=True)