# ATS Resume Analyzer

ATS Resume Analyzer Expert is a Streamlit-based application designed to assist job seekers and HR professionals by analyzing resumes against job descriptions. Utilizing the power of Google's Generative AI model "gemini-pro-vision", it offers insights and recommendations to enhance the resume's alignment with specific job requirements.

## Features

- **Resume Analysis**: Evaluates how well a resume matches a given job description.
- **Skill Enhancement Recommendations**: Offers advice on improving skills based on the job's requirements.
- **Job Description and Resume Match Analysis**: Provides a percentage match and detailed analysis.
- **Cover Letter Generation**: Helps in crafting a tailored cover letter.
- **Resume Formatting Suggestions**: Offers suggestions on how to format the resume effectively.
- **Markdown Conversion**: Converts responses into a structured markdown format for professional use.

## Installation

To run the ATS Resume Expert application, follow these steps:

1. Clone the repository:

2. Navigate to the app's directory:

3. Install the required dependencies:
   - For PDFs to work correctly, Install poppler for your respective operating system from [here](https://poppler.freedesktop.org/releases.html).

4. Set up your environment variables:

- Rename `.env.example` to `.env`.
- Add your `GOOGLE_API_KEY` to the `.env` file.

5.Run the Streamlit app:

## Usage

1. **Start the Application**: Run the command `streamlit run app.py` and navigate to the provided local URL.

2. **Enter Job Description**: Paste the job description in the provided text area.

3. **Upload Resume**: Upload the resume in PDF format.

4. **Choose a Feature**: Select from the available tabs to perform different analyses or tasks.

5. **View Results**: The app will display results based on the selected feature and the provided inputs.

## Troubleshooting

If you encounter issues, especially with PDF uploads, ensure the file is not empty or corrupted. Check the error messages for specifics.

## Contributing

Contributions to enhance ATS Resume Expert are welcome. Please follow standard procedures for contributing to open-source projects.

## License

MIT
