from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/videos'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    # List all video files
    videos = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.mp4')]
    return render_template('youtube.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
            return redirect(url_for('index'))  # Redirect back to home page after uploading
    return render_template('upload.html')  # Show the upload form

@app.route('/watch/<filename>')
def watch(filename):
    return render_template('watch.html', filename=filename)

@app.route('/static/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
