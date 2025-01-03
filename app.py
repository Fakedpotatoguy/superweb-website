from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/media'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    # List all video and audio files
    media_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.mp4', '.mp3'))]
    return render_template('index.html', media_files=media_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        media = request.files['media']
        if media:
            media.save(os.path.join(app.config['UPLOAD_FOLDER'], media.filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/watch/<filename>')
def watch(filename):
    return render_template('watch.html', filename=filename)

@app.route('/listen/<filename>')
def listen(filename):
    return render_template('listen.html', filename=filename)

@app.route('/static/media/<filename>')
def serve_media(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
