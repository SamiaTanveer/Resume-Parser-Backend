
import logging
import jsonfinder
from marshmallow import ValidationError
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from schemas.validation import ResumeSchema
from pipelines.ollama import get_resume_details
from pdfminer.high_level import extract_text
from flask_cors import CORS # type: ignore


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Swagger setup
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'ollama'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Error handler for validation errors
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({'error': 'Validation Error', 'message': e.messages}), 400

# Error handler for general exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {e}")
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500

@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    try:
        print('inside the parse-resume')
        data = ResumeSchema().load(request.json)
        resume = data['resume']

        if not resume.strip():
            return jsonify({'error': 'Validation Error', 'message': 'Resume content cannot be empty'}), 400

        result = process_resume(resume)
        return jsonify({'response': result}), 200
    except ValidationError as ve:
        logging.error(f"Validation error: {ve}")
        return jsonify({'error': 'Validation Error', 'message': ve.messages}), 400
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


def process_resume(resume):
    try:
        print("inside process_resume_new")
        response = get_resume_details(resume)

        if isinstance(response, dict):
            if "error" in response:
                return response  # Return the error from LLM function
            return response

        if isinstance(response, str) and jsonfinder.has_json(response):
            extracted_json = jsonfinder.only_json(response)
            return extracted_json[2] if len(extracted_json) > 2 else {"error": "Incomplete JSON structure"}

        return {"error": "Unknown response format from LLM"}

    except Exception as e:
        logging.error(f"Error in process_resume_new: {e}")
        return {
            "error": "Processing Error",
            "message": str(e)
        }

# ✅ New API: Parse PDF into text
@app.route('/parse-pdf', methods=['POST'])
def parse_pdf():
    print("Inside the parse-pdf")
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Validation Error', 'message': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Validation Error', 'message': 'No selected file'}), 400


        if file:
            # Extract text from PDF
            text = extract_text(file.stream)
            return jsonify({'text': text}), 200

    except Exception as e:
        logging.error(f"Error parsing PDF: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@app.route('/', methods=['GET'])
def hello_from_server():
    return "Hello from the server! I am up and running"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
