import PySimpleGUI as pgui
from time import sleep
import os
from videoDownloader import VideoDownloader
import re


class Window:

    def __init__(self):
        pgui.theme("Black")
        self.titulo = ""
        self.layout1 = [
            [pgui.Text("Link:"),pgui.Input(size=(40,20),key="link")],
            [pgui.FolderBrowse(key="path"),pgui.Input(f"{os.getcwd()}",background_color="black",key="infoPath")],
            [pgui.Checkbox("create a special directory for the file?",key="dir")],
            [pgui.Text("Formats:"),pgui.Checkbox("Video",default=True,key="videoType"),pgui.Checkbox("Audio",key="audioType")],
            [pgui.ProgressBar(max_value=10000,size=(40,20),key="progresso",bar_color=(0x4CE709,0x150B02,100))],
            [pgui.Button("Download",disabled=True,button_color="#2CA900",disabled_button_color="#030303")],
            [pgui.Text("Please select a type of your link!",visible=False,key="erro1",text_color="red"),pgui.Text("Please select a format of your video!",visible=False,key="erro2",text_color="red")],
        ]
        self.layout2 =[
            [pgui.Text(f"Downloading ...",key="aviso1",visible=False)],
            [pgui.Text(f"Finished Download!",key="aviso2",visible=False)],
        ]
        self.main_layout= [
            [pgui.Column(layout=self.layout1,key="colum1")],
            [pgui.Column(layout=self.layout2,visible=False,key="colum2")],
        ] 
        self.main_size = (300,220)
        self.terminal_size = (300,300)
        self.main_window = pgui.Window("Monk Downloader",layout=self.main_layout,size=self.main_size)
        self.barra_de_progresso = self.main_window["progresso"]   

    def download(self,link="",makedir=False,diretorio="",isVideo=bool,isAudio=bool):
        self.arquivo = VideoDownloader(link=link,diretorio=diretorio)

        if makedir:
            self.arquivo.MakeDir()

        if isAudio:
            try:
                self.arquivo.downloadAudio()
                return True
            except Exception as log:
                with open("layoutLog.txt","w") as arquivo:
                    arquivo.write(f"{log}")
        elif isVideo:
            try:
                self.arquivo.videoDownload()
                return True
            except Exception as log:
                with open("layoutLog.txt","w") as arquivo:
                    arquivo.write(f"{log}")
        else:
            return self.arquivo

    def run(self):
        patternLink1 = re.compile(r"www\.youtube\.com/watch\?v=[a-zA-Z0-9]+")
        patternLink2 = re.compile(r"www.youtube.com/c/[a-zA-Z0-9]+")
        patternLink3 = re.compile(r"www\.youtube\.com/watch\?v=[a-zA-Z0-9]+\&list=")
        patterns = [patternLink1,patternLink2,patternLink3]
        while True:
            evento , valor = self.main_window.read(300)
            
            if evento == pgui.WIN_CLOSED:
                self.main_window.close()
                break

            def link():
                if not valor["link"] in ("", None):
                    for n in patterns:
                        confirmLink = re.findall(pattern=n,string=f"{valor['link']}")
                        if confirmLink:
                            return True
                return False
            ok_link = False
            if link() == True:
                ok_link = True
            else:
                ok_link = False


            if evento == "path":
                self.main_window["infoPath"].Update(f"{valor['path']}")

            #video type
            def ok2_ok2():
                if valor["videoType"] == True:
                    self.main_window["erro2"].Update(visible=False)
                    self.main_window["audioType"].Update(visible=False)
                    self.main_window["videoType"].Update(visible=True)
                elif valor["audioType"] == True:
                    self.main_window["erro2"].Update(visible=False)
                    self.main_window["audioType"].Update(visible=True)
                    self.main_window["videoType"].Update(visible=False)
                else:
                    self.main_window["audioType"].Update(visible=True)
                    self.main_window["videoType"].Update(visible=True)
                    self.main_window["erro1"].Update(visible=False)
                    self.main_window["erro2"].Update(visible=True)
                    return False
                return True


    #download and progres bar
            ok = ok2_ok2()
            if ok:
                self.main_window["Download"].Update(disabled=False)
                if evento == "Download":
                    if valor["link"] != "" and ok_link == True:
                        self.main_window["colum2"].Update(visible=True)
                        self.main_window.set_min_size(self.terminal_size)
                        self.titulo = f"{VideoDownloader(link=valor['link']).title}"
                        for i in range(10000):
                            if i in (1000,4000,6000,9999):
                                if i == 1000:
                                    self.main_window["aviso1"].Update(visible=True)
                                if i == 6000:
                                    self.main_window["aviso2"].Update(visible=True)
                                sleep(0.3)
                            if i == 2000:
                                self.download(link=valor["link"],makedir=valor["dir"],diretorio=valor["infoPath"],isVideo=valor["videoType"],isAudio=valor["audioType"])
                            self.barra_de_progresso.UpdateBar(i+1)
                        sleep(0.5)
                        self.barra_de_progresso.UpdateBar(0)
                        self.main_window["link"].Update("")
                        sleep(1.5)
                        for n in range(1,3):
                            self.main_window[f"aviso{n}"].Update(visible=False)
                        self.main_window["colum2"].Update(visible=False)
                        self.main_window.set_min_size(self.main_size)
                        continue