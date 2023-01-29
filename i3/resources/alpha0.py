import tkinter as tk
from PIL import Image, ImageTk


root = tk.Tk()
root.geometry('430x480+50+50')
root.title("Transparency Test")
root["bg"] = "black"

layer = tk.PhotoImage(file ="clippy.png")
topFrame = tk.Label(text="Ping Checker", bg="black", image=layer, fg="#fff", font="Bahnschrift 14")
topFrame.place(x=11,y=10)

topFrame.pack_forget()
topFrame.pack()
topFrame.wm_attributes("-alpha", 1)

root.wait_visibility(root)
root.wm_attributes("-alpha", 0.5)
root.mainloop()
