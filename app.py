from flask import *
import _thread
from youtube import dw_YouTube
import time
import os


    
app = Flask(__name__)
app.secret_key = "dont tell"

@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
    def delete_video(name, path):
        # video_path = current_app.root_path + "/static/youtube_videos" + name +".mp4"
        video_path = path+ "/" + name +".mp4"
        time.sleep(500)
        os.remove(video_path) 
        print("deleted",video_path)

    if request.method == 'POST':
        url = request.form["url"]
        quality = request.form["quality"]
        if (url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be")  and len(url) > 23 :
            path = current_app.root_path + "/static/youtube_videos"
            name = url[-10:]
            youtube = dw_YouTube(url, quality, path)
            msg = youtube.download_video()
            if msg == "Error":
                print('Download Error Pleas check URL')
                flash('Download Error Pleas check URL', "err")
                return redirect(url_for("youtube"))
            else : 
                _thread.start_new_thread( delete_video, (name, path) )
                flash(name, "data")
                return redirect("/youtube")

        else:
            # _thread.start_new_thread( delete_video, ('name', ) )
            flash('Pleas check URL', "err")
            return redirect(url_for("youtube"))
  
    return render_template('youtube.html')


@app.route("/insta")
def insta():
    return render_template('insta.html')



if __name__ == "__main__":
    app.run(debug=True, port=8080)