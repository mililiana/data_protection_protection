from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from my_rsa import generate_keys, encrypt_message, decrypt_message, encrypt_file, decrypt_file
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'encrypted_files'
DECRYPTED_FOLDER = 'decrypted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


PUBLIC_KEY_PATH = 'public.pem'
PRIVATE_KEY_PATH = 'private.pem'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def generate():
    generate_keys(PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)
    flash("Ключі успішно згенеровані!")
    return redirect(url_for('home'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form.get('message')
    file = request.files.get('file')

    if message:
        encrypted = encrypt_message(message, PUBLIC_KEY_PATH)
        with open(os.path.join(UPLOAD_FOLDER, 'encrypted_message.txt'), 'wb') as f:
            f.write(encrypted)
        flash("Повідомлення успішно зашифровано!")
    elif file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        encrypt_file(file_path, PUBLIC_KEY_PATH)
        flash("Файл успішно зашифровано!")

    return redirect(url_for('home'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['encrypted_file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    decrypted_path = os.path.join(DECRYPTED_FOLDER, f"decrypted_{file.filename}")
    decrypt_file(file_path, PRIVATE_KEY_PATH, decrypted_path)
    flash(f"Файл розшифровано та збережено у {decrypted_path}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
