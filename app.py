from flask import *
from werkzeug.utils import secure_filename
from main import *
import os

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/uploads/<filename>')
def serve_video(filename):
    return send_from_directory('uploads', filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get video file and keyword from form data
        video_file = request.files['videoFile']
        keyword = request.form['keyword']

        if video_file and keyword:
            filename = secure_filename(video_file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(video_path)

            # Save keyword to a text file
            keyword_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'keyword.txt')
            with open(keyword_file_path, 'w') as keyword_file:
                keyword_file.write(keyword)
            
            average_timestamp = convert_audio_to_text(video_path)
            transcript_file_path = "output.txt"
            search_word = extract_all_words_from_file(keyword_file_path)
            timestamp_value = search_word_in_transcript(search_word[0], transcript_file_path)
            print(f"Timestamp value: {timestamp_value}")
             
            base_url = request.url_root
            response_data = {'message': 'Video uploaded successfully', 'timestamp_value': timestamp_value}
            return jsonify(response_data), 200
        
        else:
            return jsonify({'error': 'Missing video file or keyword'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
