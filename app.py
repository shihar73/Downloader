from flask import *
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
    if request.method == 'POST':
        url = request.form["url"]
        quality = request.form["quality"]
        if (url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be")  and len(url) > 23 :
            path = current_app.root_path + "/static/youtube_videos"

            youtube = dw_YouTube(url, quality, path)
            msg = youtube.download_video()
            print(msg)
            if msg == "Error":
                print('Download Error Pleas check URL')
                flash('Download Error Pleas check URL', "err")
                return redirect(url_for("youtube"))
            else : 
                flash(msg, "data")
                return redirect("/youtube")

        else:
            flash('Pleas check URL', "err")
            return redirect(url_for("youtube"))
  
    return render_template('youtube.html')


@app.route("/insta")
def insta():
    return render_template('insta.html')



if __name__ == "__main__":
    app.run(debug=True)