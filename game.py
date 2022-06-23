import tkinter as tk
from tkinter import ttk


root = tk.Tk()

root.title ("Rock Paper Scissor")

window_width = 400
window_height = 400

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.attributes('-topmost', 1)
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

Rock_icon = tk.PhotoImage(file='./rock.png')
RockBtn = ttk.Button(
    root,
    text='Exit',
    image=Rock_icon,
    command=lambda: root.quit()
)
RockBtn.pack(
    ipadx=10,
    ipady=10,
    side="left",
    expand=True
)
Scissor_icon = tk.PhotoImage(file='./scissor.png')
ScissorBtn = ttk.Button(
    root,
    text='Exit',
    image=Scissor_icon,
    command=lambda: root.quit()
)
ScissorBtn.pack(
    ipadx=10,
    ipady=10,
    expand=True,
    side="left",
)
Paper_icon = tk.PhotoImage(file='./paper.png')
PaperBtn = ttk.Button(
    root,
    text='Exit',
    image=Paper_icon,
    command=lambda: root.quit()
)
PaperBtn.pack(
    ipadx=10,
    ipady=10,
    expand=True,
    side="left",
)

root.mainloop()