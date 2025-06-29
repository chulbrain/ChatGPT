from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import pdfplumber

# TODO: Replace with real summarization logic (e.g., LLM)

def summarize_text(text):
    # Placeholder summarization function
    return text[:1000] + "..."

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        file = request.files.get('paper')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with pdfplumber.open(file_path) as pdf:
                full_text = "\n".join(page.extract_text() or '' for page in pdf.pages)
            summary = summarize_text(full_text)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
