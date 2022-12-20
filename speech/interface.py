import PySimpleGUI as sg
import speech_recognition as sr
from os import path
if __name__ == '__main__':   
    layout = [
          [sg.Radio('Micro', 'group1',key='M',default=True),sg.Radio('Path', 'group1',key='P',default=False)],
          [sg.Input(key='-INPUT-')], 
          [sg.Button('Start'),sg.Button('Stop')],
          [sg.Text(size=(40,20), key='-OUTPUT-')]]

    window = sg.Window('Transcription', layout)
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
        
        if values['M'] is True:
            if event == 'Start':
                window['-OUTPUT-'].update("Press Stop to continue...")==True
                window['Start'].update(disabled=True)
                window['Stop'].update(disabled=False)
                r=sr.Recognizer()
                with sr.Microphone(device_index=1) as source:
                    r.adjust_for_ambient_noise(source)
                    audio=r.listen(source)
       
        if values['P'] is True:
            if event == 'Start':
                window['Stop'].update(disabled=True)
                try:
                    file = path.join(path.dirname(path.realpath(__file__)), values['-INPUT-'])
                    r = sr.Recognizer()
                    with sr.AudioFile(file) as source:
                        audio = r.record(source)
                    try:
                        window['-OUTPUT-'].update("Your message:" + r.recognize_google(audio,language='ru-Ru'))
                    except sr.UnknownValueError:
                        window['-OUTPUT-'].update("Could not understand audio")
                    except sr.RequestError as e:
                        window['-OUTPUT-'].update("Could not request results from Google Speech Recognition service; {0}".format(e))
                except FileNotFoundError:
                    window['-OUTPUT-'].update("No such file or directory")
        if event == 'Stop':
            window['Start'].update(disabled=False)
            try:
                query=r.recognize_google(audio,language='ru-Ru',with_confidence=False,show_all=False)
                window['-OUTPUT-'].update("Your message:"+query)
            except Exception as e: 
                window['-OUTPUT-'].update("ERROR")
            