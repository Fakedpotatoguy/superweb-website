from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/media'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    # List all video and audio files
    media_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.mp4', '.mp3'))]
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MyTube - Home</title>
            <style>
                /* General Styles */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }

                h1, h2 {
                    text-align: center;
                    color: #007BFF;
                }

                /* Navbar */
                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: #007BFF;
                    padding: 10px 20px;
                    color: white;
                }

                .navbar a {
                    text-decoration: none;
                    color: white;
                    font-size: 18px;
                    padding: 10px 15px;
                    border-radius: 5px;
                }

                .navbar a:hover {
                    background-color: #0056b3;
                }

                /* Container */
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }

                /* Media List */
                .media-list {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }

                .media-list ul {
                    list-style: none;
                    padding: 0;
                }

                .media-list li {
                    margin: 10px;
                }

                .media-link {
                    text-decoration: none;
                    font-size: 18px;
                    color: #007BFF;
                }

                .media-link:hover {
                    text-decoration: underline;
                }

                /* Buttons */
                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 5px;
                    display: block;
                    margin: 20px auto;
                }

                button:hover {
                    background-color: #0056b3;
                }

                /* Media Player */
                .media-container {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }

                audio, video {
                    width: 100%;
                    max-width: 800px;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="/" class="home-btn">Home</a>
                <a href="/upload" class="upload-btn">Upload a Media File</a>
            </div>

            <div class="container">
                <h1>Welcome to MyTube</h1>
                <h2>Available Media</h2>
                <div class="media-list">
                    {% if media_files %}
                        <ul>
                            {% for media in media_files %}
                                <li>
                                    {% if media.endswith('.mp4') %}
                                        <a href="{{ url_for('watch', filename=media) }}" class="media-link">{{ media }}</a>
                                    {% else %}
                                        <a href="{{ url_for('listen', filename=media) }}" class="media-link">{{ media }}</a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <p>No media uploaded yet. Please upload a media file.</p>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
    ''', media_files=media_files)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        media = request.files['media']
        if media:
            media.save(os.path.join(app.config['UPLOAD_FOLDER'], media.filename))
            return redirect(url_for('index'))
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Upload Media</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }

                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: #007BFF;
                    padding: 10px 20px;
                    color: white;
                }

                .navbar a {
                    text-decoration: none;
                    color: white;
                    font-size: 18px;
                    padding: 10px 15px;
                    border-radius: 5px;
                }

                .navbar a:hover {
                    background-color: #0056b3;
                }

                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }

                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 5px;
                    display: block;
                    margin: 20px auto;
                }

                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="/" class="home-btn">Home</a>
            </div>

            <div class="container">
                <h1>Upload a Media File</h1>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <label for="media">Choose a Media File (video/audio):</label>
                    <input type="file" name="media" accept="video/*,audio/*" required>
                    <button type="submit">Upload Media</button>
                </form>
                <br>
                <a href="/" class="home-btn">Back to Home</a>
            </div>
        </body>
        </html>
    ''')


@app.route('/watch/<filename>')
def watch(filename):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Watch Video</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }

                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: #007BFF;
                    padding: 10px 20px;
                    color: white;
                }

                .navbar a {
                    text-decoration: none;
                    color: white;
                    font-size: 18px;
                    padding: 10px 15px;
                    border-radius: 5px;
                }

                .navbar a:hover {
                    background-color: #0056b3;
                }

                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }

                .media-container {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }

                video {
                    width: 100%;
                    max-width: 800px;
                }

                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 5px;
                    display: block;
                    margin: 20px auto;
                }

                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="/" class="home-btn">Home</a>
            </div>

            <div class="container">
                <h1>Now Watching: {{ filename }}</h1>
                <div class="media-container">
                    <video controls width="800">
                        <source src="{{ url_for('serve_media', filename=filename) }}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
                <br>
                <a href="/" class="home-btn">Back to Home</a>
            </div>
        </body>
        </html>
    ''', filename=filename)


@app.route('/listen/<filename>')
def listen(filename):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Listen Audio</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }

                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: #007BFF;
                    padding: 10px 20px;
                    color: white;
                }

                .navbar a {
                    text-decoration: none;
                    color: white;
                    font-size: 18px;
                    padding: 10px 15px;
                    border-radius: 5px;
                }

                .navbar a:hover {
                    background-color: #0056b3;
                }

                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }

                .media-container {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }

                audio {
                    width: 100%;
                    max-width: 800px;
                }

                button {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 5px;
                    display: block;
                    margin: 20px auto;
                }

                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="/" class="home-btn">Home</a>
            </div>

            <div class="container">
                <h1>Now Listening: {{ filename }}</h1>
                <div class="media-container">
                    <audio controls>
                        <source src="{{ url_for('serve_media', filename=filename) }}" type="audio/mp3">
                        Your browser does not support the audio tag.
                    </audio>
                </div>
                <br>
                <a href="/" class="home-btn">Back to Home</a>
            </div>
        </body>
        </html>
    ''', filename=filename)


@app.route('/static/media/<filename>')
def serve_media(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
