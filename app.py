from flask import *
import time


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
        if url[:23] == "https://www.youtube.com" and len(url) > 23:
            print(url, quality)
            print(len(url))
            return redirect("/youtube")
        else:
            flash('Pleas check URL')
            return redirect(url_for("youtube"))

    return render_template('youtube.html')

@app.route("/insta")
def insta():
    return render_template('insta.html')



if __name__ == "__main__":
    app.run(debug=True, port=8080)