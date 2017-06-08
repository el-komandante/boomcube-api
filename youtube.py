import pafy
import os
from ffmpy import FFmpeg
from flask import Flask, request, send_from_directory
# from flask_socketio import ocketIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def pull_video():
    # print request.json
    data = request.get_json()
    video = pafy.new(data['video_url'])
    best_audio = video.getbestaudio()
    filename = video.videoid + '.' + best_audio.extension
    if os.path.isfile('./videos/' + video.videoid + '.wav'):
        print 'file is already downloaded'
    else:
        best_audio.download(filepath=filename, quiet=True)
        ff = FFmpeg(
            global_options=['-loglevel quiet'],
            executable='/usr/local/bin/ffmpeg',
            inputs={filename: None},
            outputs={'./videos/' + video.videoid + '.wav': None}
        )
        ff.run()
        os.remove(filename)
    return send_from_directory('videos', video.videoid + '.wav')

if __name__ == '__main__':
    app.run()

# CHUNK = 1024
