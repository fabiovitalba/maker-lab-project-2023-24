import customtkinter as ctk
from pandastable import Table

def item_list_window(win_height, win_width, button_font, items_df):
    il_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(il_window, height=win_height, width=win_width)

    button_width = 900
    button_height = 100
    
    quit_button = ctk.CTkButton(il_window, text="Back", command=il_window.destroy, width=button_width, height=button_height, font=button_font)
    quit_button.pack(pady=10)

    table = Table(canvas, dataframe=items_df, showtoolbar=False, showstatusbar=True, width=win_width-20, height=win_height-150)
    table.pack(pady=10)
    canvas.pack()
