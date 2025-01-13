
from flask import Flask, render_template, request
from md5 import md5, md5_padding
from md5_hashlib import md5_builtin


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hash', methods=['POST'])
def hash_message():
    option = request.form.get('option')
    message = request.form.get('message', '')
    file = request.files.get('file', None)
    md5file = request.files.get('md5file', None)

    custom_md5 = None
    builtin_md5 = None
    file_md5 = None
    md5_file_check = None

    if option == 'text':
        padded_message = md5_padding(message.encode())
        custom_md5 = md5(padded_message).upper()
        builtin_md5 = md5_builtin(message.encode()).upper()
        save_hash_to_file('hash_result.txt', custom_md5, builtin_md5, None)

    elif option == 'file' and file:
        file_content = file.read()
        file_md5 = md5_builtin(file_content).upper()
        if md5file:
            md5_hash_content = md5file.read().decode('utf-8').strip().upper()
            md5_file_check = (file_md5 == md5_hash_content)
        save_hash_to_file('file_hash_result.txt', None, None, file_md5)

    return render_template('index.html',
                           custom_md5=custom_md5,
                           builtin_md5=builtin_md5,
                           match=(custom_md5 == builtin_md5) if custom_md5 and builtin_md5 else None,
                           file_md5=file_md5,
                           md5_file_check=md5_file_check,
                           form_submitted=True)


def save_hash_to_file(filename, custom_hash, builtin_hash, file_hash):
    with open(filename, 'w') as f:
        if custom_hash:
            f.write(f"Custom MD5: {custom_hash}\n")
        if builtin_hash:
            f.write(f"Built-in MD5: {builtin_hash}\n")
        if file_hash:
            f.write(f"File MD5: {file_hash}\n")

if __name__ == '__main__':
    app.run(debug=True)
