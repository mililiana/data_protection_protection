# app.py
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from dsa import generate_keys, save_key_to_file, load_private_key, load_public_key, sign_message, sign_file, verify_signature, verify_file_signature
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    private_key, public_key = generate_keys()
    save_key_to_file(private_key, 'private_key.pem')
    save_key_to_file(public_key, 'public_key.pem', is_private=False)
    flash("Keys generated and saved as 'private_key.pem' and 'public_key.pem'.")
    return redirect(url_for('index'))

@app.route('/sign_message', methods=['POST'])
def sign_message_route():
    message = request.form.get('message')
    private_key = load_private_key('private_key.pem')
    signature = sign_message(private_key, message)
    with open('message_signature.txt', 'wb') as f:
        f.write(signature)
    flash(f"Message signed. Signature saved to file")
    return redirect(url_for('index'))

@app.route('/sign_file', methods=['POST'])
def sign_file_route():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        private_key = load_private_key('private_key.pem')
        signature = sign_file(private_key, file_path)
        with open(f"{file.filename}_signature.txt", 'wb') as f:
            f.write(signature)
        flash(f"File signed. Signature saved as {file.filename}_signature.txt")
    return redirect(url_for('index'))

@app.route('/verify_message', methods=['POST'])
def verify_message_route():
    message = request.form.get('message')
    public_key = load_public_key('public_key.pem')
    with open('message_signature.txt', 'rb') as f:
        signature = f.read()
    result = verify_signature(public_key, message, signature)
    flash("Signature is valid." if result else "Signature is invalid.")
    return redirect(url_for('index'))

@app.route('/verify_file', methods=['POST'])
def verify_file_route():
    file = request.files['file']
    signature_file = request.files['signature_file']
    if file and signature_file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        signature = signature_file.read()
        public_key = load_public_key('public_key.pem')
        result = verify_file_signature(public_key, file_path, signature)
        flash("Signature is valid." if result else "Signature is invalid.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
