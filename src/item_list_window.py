import customtkinter as ctk
import pandas as pd
from CTkTable import *

TABLE_ITEM_FONT = ("Helvetica", 18, "bold")

def item_list_window(win_height, win_width, button_font, items_df):
    il_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(il_window, height=win_height, width=win_width)

    button_width = 900
    button_height = 100
    
    quit_button = ctk.CTkButton(il_window, text="Back", command=il_window.destroy, width=button_width, height=button_height, font=button_font)
    quit_button.pack(pady=10)

    items_df_reduced = items_df.loc[ : , ['Description', 'Expiration Date', 'Quantity'] ]
    items_df_reduced.sort_values(by=['Expiration Date'], inplace=True)
    items_df_reduced['Expiration Date'] = pd.to_datetime(items_df_reduced['Expiration Date'], unit='s').dt.strftime('%B %d, %Y')
    table_values = [items_df_reduced.columns.tolist()] + items_df_reduced.values.tolist()
    #TODO: Add colors: Either as DF column or somehow else --> The CTkTable library is very small, we can copy and adapt it
    table = CTkTable(master=il_window, row=len(table_values), column=3, values=table_values, font=TABLE_ITEM_FONT)
    table.pack(expand=False, fill="both", padx=20, pady=20)
    canvas.pack()
