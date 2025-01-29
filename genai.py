from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

os.environ["GOOGLE_API_KEY"] = "AIzaSyC2YrVBBOjZuM_SJew9BLX6CllTpwP8Y84"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML


@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')

    # The model's response is returned in markdown format (you can return it as is)
    prompt = f"""
    You are a professional speech therapist and critic. Your task is to evaluate the given speech transcript for grammatical and pronunciation mistakes. Assign a score based on the correctness, fluency, and clarity of the speech. 

    ### **Response Formatting Guidelines:**  
    - Wrap all **headings** (`Score`, `Grammar Issues`, etc.) in `<h2>` tags with the class **"output-heading"**  
    - Wrap **grammar and pronunciation issues** in `<ul>` tags with the class **"output-ul"** and use `<li>` for each issue  
    - Wrap **suggestions and areas needing improvement** in `<ul>` with the class **"output-ul"**  
    - Wrap all **explanatory text** in `<p>` tags with the class **"output-p"**  

    ### **Evaluation Criteria:**  
    - **Grammar**: Identify and highlight any grammatical errors.  
    - **Coherence & Flow**: Evaluate whether ideas are connected logically and smoothly.  
    - **Fluency & Clarity**: Assess how smoothly the speech flows.  
    - **Readability & Engagement**: Check if the speech is easy to follow and engaging.
    - **Overall Score**: Provide a numerical score (out of 10) and justify the given score.  

    ### **Expected Output Format (HTML):**  
    ```html
    <h2 class="output-heading">Score: [Score]</h2>

    <h2 class="output-heading">Grammar Issues:</h2>
    <ul class="output-ul">
    <li>[List of grammar issues]</li>
    </ul>

    <h2 class="output-heading">Coherence & Flow:</h2>
    <ul class="output-ul">
    <li>[Issues with logical flow or disconnected ideas]</li>
    </ul>

    <h2 class="output-heading">Readability & Engagement:</h2>
    <ul class="output-ul">
    <li>[Suggestions for making the speech more engaging]</li>
    </ul>

    <h2 class="output-heading">Suggestions for Improvement:</h2>
    <ul class="output-ul">
    <li>[Improvement suggestions]</li>
    </ul>

    <h2 class="output-heading">Areas Needing Improvement:</h2>
    <ul class="output-ul">
    <li>[Areas needing improvement]</li>
    </ul>

    <p class="output-p">Response Analysis: [Provide an overall assessment of the speech]</p>

    Response: {user_message}

    
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

 
    generated_text = response.text  # Extract the content as a string

    # Trim the ``` and `html` from the generated text
    trimmed_text = generated_text.strip('`html\n')

    print(trimmed_text)


    return jsonify({"response": trimmed_text})

if __name__ == "__main__":
    app.run(debug=True)

