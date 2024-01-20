from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def extract_field_from_description(description):
    return "Extracted Field"


def construct_prompt(template, field):
    return template.replace("[User-Specified Field]", field)


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Reset the file pointer to the start of the file
        uploaded_file.seek(0)

        # Read the file content
        file_content = uploaded_file.read()

        # Check if the file content is not empty
        if file_content:
            try:
                images = pdf2image.convert_from_bytes(file_content)
                first_page = images[0]

                # Convert to bytes
                img_byte_arr = io.BytesIO()
                first_page.save(img_byte_arr, format="JPEG")
                img_byte_arr = img_byte_arr.getvalue()

                pdf_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode(),
                    }
                ]
                return pdf_parts
            except pdf2image.exceptions.PDFPageCountError as e:
                raise e
        else:
            raise ValueError("Uploaded file is empty or invalid.")
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area(
    "Job Description: ", key="input", placeholder="Paste the job description here..."
)
uploaded_file = st.file_uploader("Upload your resume(PDF)", type=["pdf"])


if "input_text" not in st.session_state:
    st.session_state["input_text"] = input_text

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = uploaded_file


if uploaded_file is not None:
    st.write("PDF uploaded successfully!")

input_prompt1 = """As an HR professional with experience in [User-Specified Field], analyze the submitted resume against the provided job description. Offer a detailed evaluation of the candidate's suitability for the role in [User-Specified Field], highlighting key strengths and areas for development. Format the response in markdown, including a table for skills and experiences pertinent to the job.
                 """

input_prompt2 = """Using your HR background in [User-Specified Field], assess the resume in relation to the job description. Provide feedback on the candidate's qualifications and recommend areas for skill enhancement relevant to [User-Specified Field]. Present your advice in markdown format. 
                 """
input_prompt3 = """Function as an ATS scanner with expertise in [User-Specified Field], and evaluate how well the resume aligns with the job description. Offer a percentage match, followed by a detailed markdown analysis. Include a two-column table for 'Keywords Used' and 'Keywords Missing', relevant to [User-Specified Field]."""

input_prompt4 = """Revamp the candidate's resume to align it with the job description in [User-Specified Field]. Focus on presenting the candidate's strengths and suitability for the role clearly and professionally in markdown format."""

input_prompt5 = """Revise and format the candidate's resume, ensuring it aligns effectively with the job description. Focus on clarity, relevance, and professional presentation. Structure the resume in a way that highlights the candidate's strengths and suitability for the role, using a markdown format for easy readability and a polished look."""


field = extract_field_from_description(input_text)

dynamic_prompt1 = construct_prompt(input_prompt1, field)
dynamic_prompt2 = construct_prompt(input_prompt2, field)
dynamic_prompt3 = construct_prompt(input_prompt3, field)
dynamic_prompt4 = construct_prompt(input_prompt4, field)
dynamic_prompt5 = construct_prompt(input_prompt5, field)


# Check if both the job description and the PDF file are provided
if input_text and uploaded_file:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        is_pdf_valid = True
    except pdf2image.exceptions.PDFPageCountError:
        st.error("Error processing the PDF file. Please upload a valid PDF.")
        is_pdf_valid = False

    if is_pdf_valid:
        # Process for each tab if PDF is valid
        field = extract_field_from_description(input_text)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Analyze Resume",
                "Skill Recommendations",
                "Analysis",
                "Cover Letter",
                "Resume Format",
            ]
        )

        with tab1:
            st.header("Analyze Resume Fit for the Job")
            if uploaded_file is not None:
                # pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(dynamic_prompt1, pdf_content, input_text)
                st.write(response)
            else:
                st.write("Please upload the resume")

        with tab2:
            st.header("Skill Enhancement Recommendations")
            if uploaded_file is not None:
                # pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(dynamic_prompt2, pdf_content, input_text)
                st.write(response)
            else:
                st.write("Please upload the resume")

        with tab3:
            st.header("Job Description and Resume Match Analysis")
            if uploaded_file is not None:
                # pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(dynamic_prompt3, pdf_content, input_text)
                st.write(response)
            else:
                st.write("Please upload the resume")
        with tab4:
            st.header("Generate Tailored Cover Letter")
            if uploaded_file is not None:
                # pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(dynamic_prompt4, pdf_content, input_text)
                st.write(response)
            else:
                st.write("Please upload the resume")
        with tab5:
            st.header("Create an Updated Resume Format")
            if uploaded_file is not None:
                # pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(dynamic_prompt5, pdf_content, input_text)
                st.write(response)
            else:
                st.write("Please upload the resume")

else:
    st.write("Please provide the job description and upload the resume PDF.")
