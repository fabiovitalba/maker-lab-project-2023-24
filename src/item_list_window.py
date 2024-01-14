import customtkinter as ctk
from CTkTable import *

def item_list_window(win_height, win_width, button_font, items_df):
    il_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(il_window, height=win_height, width=win_width)

    button_width = 900
    button_height = 100
    
    quit_button = ctk.CTkButton(il_window, text="Back", command=il_window.destroy, width=button_width, height=button_height, font=button_font)
    quit_button.pack(pady=10)

    table = CTkTable(master=il_window, row=len(items_df), column=5, values=items_df.values.tolist())
    table.pack(expand=True, fill="both", padx=20, pady=20)
    canvas.pack()
