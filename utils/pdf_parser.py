# We import PyPDF2, which is a tool specifically built to read PDF files
import PyPDF2

def extract_text_from_pdf(file_path):
    """
    This function takes the location of a PDF file, opens it, 
    reads all the pages, and returns the text inside it.
    """
    # We create an empty string variable to hold our text
    extracted_text = ""
    
    try:
        # 1. Open the file in "rb" (read binary) mode
        with open(file_path, "rb") as file:
            # 2. Tell PyPDF2 to read the file
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 3. Loop through every single page in the resume
            for page in pdf_reader.pages:
                # 4. Extract the text from the page and add it to our variable
                extracted_text += page.extract_text() + "\n"
                
        # 5. Return the final extracted text
        return extracted_text
        
    except Exception as error:
        # If something goes wrong (like the file doesn't exist), return an error message
        return f"Error reading the PDF: {error}"

# --- Test Area ---
# The code below only runs if we execute this specific file.
# It is a good habit to test our functions immediately.
if __name__ == "__main__":
    print("PDF Parser is ready to use!")
    # Later, we will test this by giving it a real resume file.