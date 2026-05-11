import tkinter as tk

root = tk.Tk()

root.title("Yocto Python GUI")
root.geometry("400x200")

label = tk.Label(
    root,
    text="Hello Yocto Python GUI!",
    font=("Arial", 18)
)

label.pack(expand=True)

root.mainloop()
