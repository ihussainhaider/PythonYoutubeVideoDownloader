import ffmpeg
from pytube import YouTube
import subprocess, tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import threading


#default path for the video to download to
dpath = 'C:/Users/Hassan Abbas/PycharmProjects/FinalProject/newProject/temporary'

'''
    function for loading the footer of the app
'''
def loadFooter(w):
    loadFooter = Image.open("footer.jpg")
    res = loadFooter.resize((400, 45))
    render = ImageTk.PhotoImage(res)
    footerLabel = Label(w, image=render)
    footerLabel.image = render
    footerLabel.place(x=-2, y=453)

'''
    fucntion for loading the header of the app
'''
def loadHeader(w):
    loadHeader = Image.open("title.jpg")
    res = loadHeader.resize((410, 60))
    render = ImageTk.PhotoImage(res)
    titleLabel = Label(w, image=render)
    titleLabel.image = render
    titleLabel.pack()

#=================================================================
#===================================================================

'''
    function for the  Tkinter app to run
'''
def app():
    '''
        creating tkinter window and specifying its title, size, cbackground color
    '''
    window = tkinter.Tk()
    window.title("BAKA Video Downloader")
    window.geometry('400x500')
    window.config(bg='#2B2A2A')
    window.resizable(False, False)
    '''
        calling the loadHeader to load the header of the app which is label with title and logo of the app
    '''
    loadHeader(window)

    '''
        adding labels which tell the user where to enter the link and qaulity
    '''
    enterLinkLabel = Label(window, text="Enter Link here", bg='#2B2A2A', fg='white')
    enterLinkLabel.place(x=50, y=180)

    enterQualityLabel = Label(window, text="Enter Quality", bg='#2B2A2A', fg='white')
    enterQualityLabel.place(x=50, y=230)

    '''
        adding entry to the window o the user can enter the link and resolution of the video
        enterLink =  to enter the link of the video
        enterQuality = to enter the resolution of the video
    '''
    enterLink = Entry(window, bd=5, width=50)
    enterLink.place(x=50, y=200)

    '''
        displaying a example text for the user in the entry widget
    '''
    enterLink.insert(END, 'for example: https://www.youtube.com/watch')

    '''
        this function will clear the entry widget upon clicking
    '''
    def clearLink(en):
        enterLink.delete(0, 'end')
    '''
        binding entry widget with click 
    '''
    enterLink.bind("<FocusIn>", clearLink)



    enterQuality = Entry(window, bd=5, width=50)
    enterQuality.place(x=50, y=250)

    '''
       displaying a example text for the user in the entry widget
    '''
    enterQuality.insert(END, 'for example: 360, 420, 720, 1080')

    '''
        this function will clear the entry widget upon clicking
    '''
    def clearQuality(a):
        enterQuality.delete(0, 'end')

    '''
        binding entry widget with click 
    '''
    enterQuality.bind("<FocusIn>", clearQuality)

    '''
        function for download button command it will execute when the button is clicked
    '''
    def downloadClicked():
        # get the url from the enterLink entry widget
        link=enterLink.get()
        # getting the resolution from the EnterQuality entry widget
        quality=enterQuality.get()

        # checking if the user have enter both the link and resolution of video
        if link and quality:
            '''
                clearing the enterLink and enterQuality entry widget
            '''
            enterQuality.delete(0, 'end')
            enterLink.delete(0, 'end')

            '''
                starting a new thread and calling the downloadYoutube function 
                so that download runs in a separate thread and the app runs in a separate thread
            '''
            threading.Thread(target=downloadYoutube, args=(link, quality+'p', dpath)).start()

        else:
            #displaying a message dialog box if the user miss a link or quality
            messagebox.showinfo("information", "url or quality is missing")
            print("link or qaulity missing")

    '''
        adding a download button to the window
    '''
    downloadButton = Button(window, text='DOWNLOAD',fg= 'white', bg='red', command= downloadClicked)
    downloadButton.place(x=160, y=290)

    '''
        calling a loadFooter function to add the add footer label to window
        which display a short message
    '''
    loadFooter(window)

    '''
        executing the mainloop function to keep the app running
    '''
    window.mainloop()


#=================================================================
#===================================================================

''' function for downloading the video with three parameters
    url = link of the video
    quality = video resolution
    path =  location to save the video
'''
def downloadYoutube(url, quality,path):
    #exception handling if the video link is valid or not
    try:
        video = YouTube(url)
    except:
        print("invalid url")
        return

    #getting the video title
    videoTitle= video.title+'.mp4'

    #getting all the streams of video
    allStreams = video.streams.order_by('itag')

    #separately saving the progressive streams
    progrssiveStreams = allStreams.filter(progressive=True)

    # separately saving the non-progressive streams
    nonProgrossiveStreams = allStreams.filter(adaptive=True)

    # separately saving the mp4 format video streams
    mp4Streams = nonProgrossiveStreams.filter(mime_type='video/mp4')

    # separately saving the mp4 format aduio streams
    mp4AudioStream = nonProgrossiveStreams.get_audio_only()

    # separately saving the webm format  video streams
    webmStreams = nonProgrossiveStreams.filter(mime_type='video/webm')

    # separately saving the webm format audio streams
    webmAudioStream = nonProgrossiveStreams.filter(mime_type='audio/webm')

    #checking if stream  of video of the resolution provided by user is available in progressive streams
    if progrssiveStreams.filter(resolution=quality):
        #displaying a dialog box to indicate that the stream is availble download is started
        messagebox.showinfo("information", "Video download start")

        # getting the required resolution stream by filtering the progressive streams list
        videostream = progrssiveStreams.get_by_resolution(quality)
        print("Downloading.....")

        '''
            downloading the video with download function and passing download location path and filename as argument
        '''
        videostream.download(output_path='C:/Users/Hassan Abbas/PycharmProjects/FinalProject/newProject/Video',filename= video.title)
        print("Download Complete!")

    else:
        '''
            two path for audio and video files becasue in non-progressive streams audio and video are in separate streams
            so thats why we have two path variables so that to later merge them 
        '''
        videoPath = './temporary/video'
        audioPath = './temporary/audio'

        '''
            in non progressive streams there are two type of video streams mp4 and webm format streams
            so we first check if the stream is available in the mp4 streams and if its avaible then download it else
            we check it in the webm format streams 
        '''
        if mp4Streams.filter(resolution=quality):
            # displaying a dialog box to indicate that the stream is availble download is started
            messagebox.showinfo("information", "Video download Start....")

            print("downloding mp4")

            # getting the required resolution stream by filtering the non-progressive mp4 streams list
            videostream = mp4Streams.filter(resolution=quality )[0]

            '''
                downloading the video file with download function and passing download location path and filename as argument
            '''
            videostream.download(output_path=path, filename='video')

            '''
                downloading the audio file with download function and passing download location path and filename as argument
            '''
            mp4AudioStream.download(output_path=path,filename='audio')
            print("Download Complete!")

            #creating ffmpeg command by concatenating it with audio and video files path and output path
            executeff = 'ffmpeg -i "' + videoPath + '.mp4" -i "' + audioPath + '.mp4" -c:v copy -c:a copy -y "./Video/' + videoTitle + '"'

            print(executeff)

            #executing the ffmpeg command with subprocess to merge the video and video files into one file
            subprocess.call(executeff)

        elif webmStreams.filter(resolution=quality):
            # displaying a dialog box to indicate that the stream is availble download is started
            messagebox.showinfo("information", "Video download Start....")
            print("donwloading webm")

            # getting the required resolution stream by filtering the non-progressive webm streams list
            videostream = webmStreams.filter(resolution=quality)[0]

            '''
                 downloading the video file with download function and passing download location path and filename as argument
            '''
            videostream.download(output_path=path,filename='video')

            '''
                downloading the audio file with download function and passing download location path and filename as argument
                the webm streams list have three audio streams so we download the high quality stream whic is last one
            '''
            webmAudioStream[2].download(output_path=path,filename='audio')
            print("Download Complete!")

            # creating ffmpeg command by concatenating it with audio and video files path and output path
            executeff = 'ffmpeg -i "' + videoPath + '.webm" -i "' + audioPath + '.webm" -c:v copy -c:a copy -y "./Video/' + videoTitle + '"'
            print(executeff)

            # executing the ffmpeg command with subprocess to merge the video and video files into one file
            subprocess.call(executeff)

    print('bye')

    # displaying message dialog box to indicate that the download is complete
    messagebox.showinfo("information", "Video download Complete")


if __name__=="__main__":
    app()