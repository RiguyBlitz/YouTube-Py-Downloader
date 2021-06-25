import requests, tkinter, os, datetime
from pytube import YouTube
from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import subprocess, sys

#functions

# https://stackoverflow.com/a/17317468 lol
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def check():
    option = value_inside.get()
    if(option == "Video"):
        video_module()
    elif(option == "Playlist"):
        pass

def video_module():
    #close welcome screen
    root.destroy()

    #create stream variable
    videos = []

    #create folder for downloads
    if(not os.path.isdir('video_downloads')):
        os.makedirs('video_downloads')

    #set youtube stuff
    yt = YouTube(value.get())
    thumbnail = yt.thumbnail_url
    video_title = yt.title

    if(len(video_title) > 70):
        width = 450 + (len(video_title) + 10)
    else:
        width = 450

    views = yt.views
    publish_date = yt.publish_date

    #set youtube streams to avc1 only
    streams = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True)
    for stream in streams:
        if stream.video_codec.startswith('avc1'):
            videos.append(stream)

    #grab resolutions
    resolutions = []
    for video_resolutions in videos:
        resolutions.append(str(video_resolutions.resolution) + ' ' + str(video_resolutions.fps) + 'fps')

    #create window
    video_window = Tk(className=" YoutubePY Downloader")
    video_window.geometry(str(width) + "x475")
    video_window.resizable(height=False, width=False)

    #create frames
    frame1 = Frame(video_window)
    frame2 = Frame(video_window)

    #download thumbnail
    with open('img.png', 'wb') as handle:
        response = requests.get(thumbnail, stream=True)

        if not response.ok:
            pass
        
        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    #create canvas
    canvas = Canvas(frame1, width = 320, height = 200)
    image = Image.open("img.png")
    image = image.resize((320, 180), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(image, master=video_window)
    canvas.create_image(20, 20, anchor=NW, image=my_img)

    #create widgets
    title = Label(frame1, text="Title: " + video_title, font="Arial 10 bold")
    views = Label(frame1, text="Views: " + str(views), font="Arial 10 bold")
    date = Label(frame1, text="Date: " + str(publish_date), font="Arial 10 bold")

    video_types = ["Video and Audio", "Just Video", "Just Audio"]
    inside_display_option_text = tkinter.StringVar(video_window)
    inside_display_option_text.set("Choose Video Type")
    display_option_text = OptionMenu(frame2, inside_display_option_text, *video_types)

    download_button = Button(frame2, text="Download", font="Arial 10", command=lambda: download_video(
    inside_display_option_text.get(),
    resolutions_options.get(),
    videos,
    ))

    resolutions_options = tkinter.StringVar(video_window)
    resolutions_options.set("Choose Quality")
    display_quality_text = OptionMenu(frame2, resolutions_options, *resolutions)

    #grid widgets
    frame1.grid(row=0, column=0, pady=(10, 15))
    frame2.grid(row=1, column=0)

    title.grid(row=1, column=0,pady=(10,5))
    views.grid(row=2, column=0,pady=(5,5))
    date.grid(row=3, column=0,pady=(5,5))

    download_button.grid(row=4, column=0,pady=(5,5))

    display_option_text.grid(row=0, column=0,pady=(5,5))
    display_quality_text.grid(row=1, column=0, pady=(5,5))
    
    canvas.grid(row=0, column=0)
    video_window.mainloop()

def download_video(type, quality, stream_options):
    video = []
    now = datetime.datetime.now()
    date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)

    if(type == 'Just Video'):
        for v in stream_options:
            if(v.resolution.startswith(quality)):
                video.append(v)
        video[0].download(output_path='video_downloads', filename=date)
        open_file(Path('video_downloads/' + date + '.mp4'))
        os.remove('img.png')
    elif(type == 'Just Audio'):

        audio_yt = YouTube(value.get())
        audio = audio_yt.streams.get_audio_only()

        file_download_name_mp4 = Path('video_downloads/' + date + '.mp4')
        file_download_name_mp3 = Path('video_downloads/' + date + '.mp3')

        audio.download(output_path='video_downloads', filename=date)

        os.rename(file_download_name_mp4, file_download_name_mp3)
        open_file(file_download_name_mp3)
        os.remove('img.png')

    elif(type == "Video and Audio"):
        pass

    
#create main window
root = Tk(className=" YoutubePY Downloader")
root.geometry("500x300")
root.resizable(height=False, width=False)
root.call('wm', 'iconphoto', root._w, PhotoImage(file=Path('Images/windowlogo.png')))

#create canvas and open image
canvas = Canvas(root, width = 256, height = 144)
image = Image.open(Path("Images/pythonyoutubedownloader.png"))
image = image.resize((256, 144), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(image)
canvas.create_image(20, 20, anchor=NW, image=my_img)

#create widgets
text1 = Label(root, text="YoutubePY Downloader", font="Arial 15 bold")
text2 = Label(root, text="Insert URL here",font="Arial 15 bold")

button1 = Button(root, text="Parse Link", command=lambda: check())

options = ["Video", "Playlist"]
value_inside = tkinter.StringVar(root)
value_inside.set("Video or Playlist?")
option_menu = OptionMenu(root, value_inside, *options)

value = tkinter.StringVar(root)
entry1 = Entry(root, textvariable=value)

#place widgets on main window
canvas.place(relx=0.49, rely=0.1, anchor=CENTER)

text1.place(relx=0.533, rely=0.35, anchor=CENTER)
text2.place(relx=0.519, rely=0.65, anchor=CENTER)

option_menu.place(relx=0.515, rely=0.5, anchor=CENTER)

entry1.place(relx=0.515, rely=0.74, anchor=CENTER)

button1.place(relx=0.515, rely=0.85, anchor=CENTER)

root.mainloop()