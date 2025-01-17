import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import socket
import threading

# Server information
HOST = '127.0.0.1'  #use loopback address
PORT = 65432        #random port

# initialize the speech recognition
recognizer = sr.Recognizer()
is_listening = False 


def start_recognition(): #starts the sr
    global is_listening
    is_listening = True
    start_button.config(text="Stop", bg = "red", command=stop_recognition)
    threading.Thread(target=listen_speech).start()

def stop_recognition(): #stops the sr
    global is_listening
    is_listening = False
    start_button.config(text="Start", bg = "lightgreen", command=start_recognition)

def listen_speech(): #listen to speech then outputs it to textbox
    global is_listening
    last_recognized_text = ""
    while is_listening:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration = 0.2)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                text = text.lower()

                if text != last_recognized_text:  # avoid duplicates
                    text_box.insert(tk.END, text)
                    text_box.insert(tk.END, ".\n")
                    last_recognized_text = text 

        except sr.UnknownValueError:
            pass
        
def reset_text():
    text_box.delete("1.0", tk.END)
    status_label.config(text="")

def clear_status_label():
    status_label.config(text="")

def send_text():
    text = text_box.get("1.0", tk.END).strip() #remove trailing whitespaces
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(text.encode())
        status_label.config(text = "Sent successfully")
        root.after(3000, clear_status_label)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send text: {e}")

# Initialize the GUI
root = tk.Tk()
root.title("Speech-to-Text GUI")
root.geometry("400x300")

#textbox
text_box = tk.Text(root, wrap=tk.WORD, height=10, width=40)
text_box.pack(pady=10)

#button frame
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

#start/stop
start_button = tk.Button(button_frame, text="Start", command=start_recognition, bg="lightgreen", width=10)
start_button.pack(side=tk.RIGHT, padx=10)

#send
send_button = tk.Button(button_frame, text="Send", command=send_text, bg="lightblue", width=10)
send_button.pack(side=tk.LEFT, padx=10)


#status when sent
status_label = tk.Label(button_frame, text="", fg="green")
status_label.pack(side=tk.RIGHT, padx=10)

#reset button
reset_button = tk.Button(button_frame, text="Reset", command=reset_text, bg="yellow", width=5)
reset_button.pack(side=tk.LEFT, padx=10)

#GUI main loop
root.mainloop()
