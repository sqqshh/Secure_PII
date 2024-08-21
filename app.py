from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

# Keywords to mask (simple simulation)
PII_KEYWORDS = ["Name", "Address", "ID"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'document' not in request.files or 'method' not in request.form:
        return "No file or method selected!", 400

    file = request.files['document']
    method = request.form['method']

    if file.filename == '':
        return "No file selected!", 400

    # Save uploaded file
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Read and process the document based on user choice
    processed_filepath = process_document(filepath, method)

    return send_file(processed_filepath, as_attachment=True)

def process_document(filepath, method):
    processed_filepath = filepath.replace(".txt", f"_{method}.txt")

    with open(filepath, 'r') as file:
        content = file.read()

    # Process the document based on the method chosen
    if method == "redaction":
        for keyword in PII_KEYWORDS:
            content = content.replace(keyword, "****")
    elif method == "masking":
        for keyword in PII_KEYWORDS:
            content = content.replace(keyword, "[REDACTED]")

    with open(processed_filepath, 'w') as file:
        file.write(content)

    return processed_filepath

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
