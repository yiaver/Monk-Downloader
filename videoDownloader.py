import os
from yt_dlp import YoutubeDL as yt_dl
from yt_dlp.postprocessor import FFmpegExtractAudioPP

class VideoDownloader:
    def __init__(self,link="",diretorio=""):
        try:
            self.diretorio = diretorio
            self.link = link
            with yt_dl() as yt :
                self.info_dict = yt.extract_info(self.link,download=False)
                self.title = self.info_dict.get("title",None)
                self.extension = self.info_dict.get("ext",None)
        except KeyError:
            print(f"Erro try again")
    def MakeDir(self):
        try:
            #cria e emtra no diretorio
            if self.diretorio != "":
                os.mkdir(f"{self.diretorio}/{self.title}")
                os.chdir(f"{self.diretorio}/{self.title}")
            else:
                os.mkdir(f"{self.title}")
                os.chdir(f"{self.title}")

        except Exception as log:
            with open("log.txt","w") as arquivo:
                arquivo.write(f"{log}")

    def downloadAudio(self):
        try:
            print(f"\nDownloading: {self.title}\n")
            options = {"format":"bestaudio","ext":"mp3"}
            with yt_dl(options) as yt:
                download = yt.download(url_list=[f"{self.link}"])
                audio = FFmpegExtractAudioPP(downloader=download,preferredcodec="ba")
            print(f"\nFinished the Download of: {self.title}\n")
        
        except Exception as log :
            with open("log.txt","w") as archive:
                archive.write(f"{log}")

    def videoDownload(self):
        try:
            print(f"\nDownloading Audio :{self.title}\n")
            options = {"format":"best[height>=360]"}
            with yt_dl(options) as yt:
                download= yt.download(url_list=[f"{self.link}"])
                
            print(f"\nFinished the Download of: {self.title}\n")
        
        except Exception as log :
            with open("log.txt","w") as archive:
                archive.write(f"{log}")
