import tkinter as tk
import customtkinter as ctk

# Screen Resolution: 1024x600
ctk.set_appearance_mode("dark")

#Def callback
def button_call():
    print("Debug button click")

window = ctk.CTk()
window.geometry('1024x600')

#Write text
window_title = ctk.CTkLabel(window, text= "Fridge Inventory Management")
window_title.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

window_subtitle = ctk.CTkLabel(window, text= "D. Di Bella & F. Vitalba")
window_subtitle.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

#Create button
button = ctk.CTkButton(window, text="List items", command=button_call)
button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
button = ctk.CTkButton(window, text="Add item", command=button_call)
button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
button = ctk.CTkButton(window, text="Remove item", command=button_call)
button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
button = ctk.CTkButton(window, text="Quit", command=button_call)
button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

window.mainloop()
