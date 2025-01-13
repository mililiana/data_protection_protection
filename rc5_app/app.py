from flask import Flask, render_template, request, redirect, url_for, flash
import os
from rc5_my import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    passphrase = request.form['passphrase']
    mode = request.form['mode']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and passphrase:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            if mode == 'encrypt':
                encrypt_file(filepath, passphrase)
                flash('File encrypted successfully!')
            elif mode == 'decrypt':
                decrypt_file(filepath, passphrase)
                flash('File decrypted successfully!')
            else:
                flash('Unsupported mode')
        except Exception as e:
            flash(f'Operation failed: {str(e)}')

        return redirect(url_for('index'))

    flash('Please provide a file and passphrase.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)