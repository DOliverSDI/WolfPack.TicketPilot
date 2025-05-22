from flask import Flask, render_template, request, jsonify
from chat_log_data import ChatLogData
from ai_document_generator import generate_service_document
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_chat.html')

@app.route('/generate_document', methods=['POST'])
def generate_document():
    print("Submit button pressed: Generating service document...")  # <-- Add this line
    data = request.json
    # Extract fields from the request
    ticket_id = data.get('ticket_id', '')
    initial_request = data.get('initial_request', '')
    request_updates = data.get('request_updates', [])
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    # Create ChatLogData object from frontend data
    chat_log = ChatLogData(date, ticket_id, initial_request, request_updates)
    chat_details = chat_log.sample_chat_data

    # Generate the document
    document = generate_service_document(chat_details)

    # Save the document to a Markdown file (reuse logic from ai_document_generator.py)
    reports_dir = "generated_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"service_report_{timestamp}.md"
    filepath = os.path.join(reports_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(document)
        file_saved = True
    except Exception as e:
        file_saved = False

    return jsonify({"document": document, "file_saved": file_saved, "filename": filename})

if __name__ == '__main__':
    print("Flask app running at http://127.0.0.1:5000/")
    app.run(debug=True)
