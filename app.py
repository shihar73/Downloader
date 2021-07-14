from flask import *
import _thread
import requests
import urllib
from youtube import dw_YouTube
from instagram import DownloadInsta
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
        time.sleep(300)
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
                print('Download Error Pleas Check URL')
                flash('Download Error Pleas Check URL', "err")
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


@app.route("/insta", methods=['GET', 'POST'])
def insta():
    def delete_video(name, path):
        video_path = path + name
        time.sleep(300)
        os.remove(video_path) 
        print("deleted",video_path)

    if request.method == 'POST':
        url = request.form["url"]
        if url[0:25] == "https://www.instagram.com":
            url_1 = urllib.parse.urlparse(url)
            if len(url_1.path) >= 20:
                print("This is a privet account")
                flash('This is a privet account', "err")
                return redirect(url_for("insta"))
            else:
                path = current_app.root_path + "/static/insta_videos/"
                print(url,path)
                insta = DownloadInsta(url, path)
                msg, data =insta.download_videos()
                if msg == "error":
                    print(data)
                    flash(data, "err")
                    return redirect(url_for("insta"))

                _thread.start_new_thread( delete_video, (data, path) )
                flash(data, "data")
                return redirect("/insta")
        else:
            print('Pleas Check url')
            flash('Pleas Check URL', "err")
            return redirect(url_for("insta"))

    return render_template('insta.html')



if __name__ == "__main__":
    app.run(debug=True)