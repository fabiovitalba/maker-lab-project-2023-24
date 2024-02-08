import customtkinter as ctk
import pandas as pd
from datetime import datetime

from custom_ctktable import *   # Adapted implementation of CTKtable

from const import DESC_LBL, EXP_LBL, QTY_LBL

TABLE_ITEM_FONT = ("Helvetica", 18, "bold")


# Creates the "Item List"-View. In this view the user will see all items in their Inventory.
# Items that are expired are colored red, items that are about to expire (in < 4 days) are 
# colored orange and all the others are colored white.
# 
# This view uses an adapted version of the "CTKtable"-package.
def item_list_window(win_height, win_width, button_font, items_df):
    il_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(il_window, height=win_height, width=win_width)

    button_width = 900
    button_height = 100

    back_button = ctk.CTkButton(il_window, text="Back", command=il_window.destroy,width=button_width, height=button_height, font=button_font)
    back_button.pack(pady=10)

    items_df_reduced = items_df.loc[:, [DESC_LBL, EXP_LBL, QTY_LBL]]
    items_df_reduced.sort_values(by=[EXP_LBL], inplace=True)

    row_colors = []
    for index, row in items_df_reduced.iterrows():
        days_to_exp = (pd.to_datetime(row[EXP_LBL], unit="s") - datetime.now()).days
        if days_to_exp < 0:
            row_colors.append("red")
        elif (days_to_exp >= 0) and (days_to_exp < 4):
            row_colors.append("orange")
        else:
            row_colors.append("")

    items_df_reduced[EXP_LBL] = pd.to_datetime(items_df_reduced[EXP_LBL], unit="s").dt.strftime("%B %d, %Y")
    items_df_reduced[QTY_LBL] = items_df_reduced[QTY_LBL].astype(int)

    table_values = [items_df_reduced.columns.tolist()] + items_df_reduced.values.tolist()
    table = CustomCTkTable(master=il_window, row=len(table_values), column=3, values=table_values, font=TABLE_ITEM_FONT, row_colors=row_colors)
    table.pack(expand=False, fill="both", padx=20, pady=20)

    canvas.pack()
