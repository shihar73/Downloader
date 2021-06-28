from pytube import YouTube


class YouTube:
    def __init__(self, url, quality, name):
        self.url = url
        self.quality = quality
        self.name = name
    


    def download_video(self):
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
        select.download(self.name)
