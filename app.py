from flask import Flask, render_template, request
import openai
import fitz

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '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'

# Initialize the OpenAI API client
openai.api_key = api_key



@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    if file:
        pdf_content = extract_text_from_pdf(file)
        return pdf_content

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_experience = ''
    # Get data from the form
    if 'resume' not in request.files:
        print("Missing file")
    file = request.files['resume']
    if file.filename == '':
        print("No file selected")
    if file:
        user_experience = extract_text_from_pdf(file)
        print(user_experience)
    job_desc = request.form['job-desc']

    # Structure your data as a series of messages for the chat model
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Based on the job description for the position: '{job_desc}' and the provided \
         my resume: '{user_experience}', analyze the suitability of the resume for the job, first print the similarity \
            percentage estimation resume to job description, this is main make sure you print the percentage, and provide \
                a detailed breakdown of the strengths and weaknesses. Dont classify according to personal info, purely \
                    take only his technical data. Dont focus on what resume has and job descrisption does not have. \
                        Focus on what job description has and my resume doest have. Mainly By given resume, try \
                            to calculate workexperience in my resume and check if it is greater than or equal \
                                to the years of experience mentioned in the Job description. It is a major factor. \
                                    If this number of years condition not that means number of my work experience years \
                                        less than job work experience, directly tell I am not elgible to job.It is very important make sure you do it. write only 3 major headings 1. GIve me a number that represents Percentage match  2. Strengths  3. Weakness and the content in the headings should be in points write short \
                                            and crisp in points"}
    ]

    # Use the v1/chat/completions endpoint for "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract and print the response
    chat_response = response['choices'][0]['message']['content']
    return render_template('index.html', chat_response=chat_response)

if __name__ == '__main__':
    app.run(debug=True)
