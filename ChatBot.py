import tkinter as tk
from PIL import ImageTk, Image
from gtts import gTTS
from functools import partial
import chatlti as lti

window = tk.Tk()
window.title("ChatBot UMM")

frame1 = tk.Frame(master=window, width=1080, height=600, bg="red")
frame1.pack(fill=tk.X)

text = "Hola mi nombre es Leonardo, en que te puedo ayudar"

label1 = tk.Label(
    master=frame1,
    text="Universidad Metropolitana de Monterrey",
    bg="red",
    fg="white",
    font=("bold", 20),
)
label1.place(x=260, y=43)

img = ImageTk.PhotoImage(Image.open("./img/leo.png"))
label = tk.Label(master=frame1, image=img)
label.place(x=10, y=113)

B = tk.Button(
    master=frame1,
    text="Iniciar",
    height=5,
    width=50,
    bg="white",
    fg="red",
    command=partial(lti.TextToVoice, text),
)
B.place(x=450, y=113)

B2 = tk.Button(
    master=frame1,
    text="Preguntale a Leo",
    height=5,
    width=50,
    bg="white",
    fg="red",
    command=lti.pregunta,
)
B2.place(x=450, y=220)


window.mainloop()
