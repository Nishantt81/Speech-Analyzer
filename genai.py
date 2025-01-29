from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up Google Gen AI API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyC2YrVBBOjZuM_SJew9BLX6CllTpwP8Y84"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

@app.route('/')
def index():
    return "Speech Analyzer API is running!", 200

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Ensure JSON data is received
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400

        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        logging.info(f"Received message: {user_message}")

        # Generate AI response
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

        generated_text = response.text.strip('`html\n')  # Trim unwanted characters

        logging.info(f"Generated response: {generated_text}")

        return jsonify({"response": generated_text})

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)





