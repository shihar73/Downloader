from pytube import YouTube


class dw_YouTube:
    err = None
    def __init__(self, url, quality, name):
        self.url = url
        self.quality = quality
        self.name = name



    def download_video(self):
        print(self.url, self.quality, self.name)
        try:
            choice = self.quality
            url = self.url
            yt = YouTube(url)
            if choice == 1 :
                select = yt.streams.filter(progressive=True).first()
            elif choice == 0 or 2:
                select = yt.streams.filter(progressive=True, file_extension="mp4").last()
            elif choice == 3:
                select = yt.streams.filter(only_audio=True).first()

            # download function
            # select.download(self.name)
            self.msg = yt.title
            print("download seccess", self.msg)
            return self.msg
        except:
            print("Error downloading")
            self.msg= "Error"
            return self.msg



def main():
    url = input("enter url : ")
    c= 0
    path = "/root/Documents/web/web-develop/develop/downloader-flask/static/youtube_videos" 
    youtube =dw_YouTube(url, c, path)
    youtube.download_video()


if __name__ == "__main__":
    main()
