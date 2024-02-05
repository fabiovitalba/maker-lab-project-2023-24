import customtkinter as ctk
from adafruit_connector import remove_item
import pandas as pd

from const import BARCODE_LBL, DESC_LBL, EXP_LBL, QTY_LBL


def remove_item_window(win_height, win_width, button_font, items_df):
    ai_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(ai_window, height=win_height, width=win_width)

    button_width = 450
    button_height = 100
    label_font = ("Helvetica", 20)
    label_width = 200
    label_height = 100
    input_font = ("Helvetica", 20, "bold")
    input_width = 450
    input_height = 100
    # must be a list in order to be editable from methods
    selected_item_index = [0]

    def reset_form():
        confirm_button.configure(state="disabled")
        label.configure(text="")
        barcode_entry.delete(0, ctk.END)
        barcode_entry.focus()

    def on_barcode_change(event, item_row_index_list):
        barcode = barcode_entry.get()
        if event.keysym == "Return":
            confirm_barcode_input(item_row_index_list)

    def get_selected_items(items_df):
        barcode_value = barcode_entry.get()
        if barcode_value != "":
            selected_items = items_df.loc[items_df[BARCODE_LBL]
                                          == barcode_value]
        else:
            selected_items = items_df
        return selected_items

    def update_item_label(items_df, item_row_index):
        selected_items = get_selected_items(items_df)
        item_desc = selected_items.iloc[item_row_index][DESC_LBL]
        item_qty = selected_items.iloc[item_row_index][QTY_LBL]
        item_exp = pd.to_datetime(
            selected_items.iloc[item_row_index][EXP_LBL], unit="s").strftime("%B %d, %Y")
        quantity_entry.set(1)
        label.configure(
            text=f"{item_desc}\n{item_qty:.0f} units\nexpires on: {item_exp}")
        confirm_button.configure(state="normal")

    def update_item_index(index, delta):
        selected_items = get_selected_items(items_df)
        if index + delta < 0:
            index = len(selected_items) - 1
        elif index + delta >= len(selected_items):
            index = 0
        else:
            index = index + delta
        return index

    def move_left(item_row_index_list):
        item_row_index_list[0] = update_item_index(item_row_index_list[0], -1)
        update_item_label(items_df, item_row_index_list[0])

    def move_right(item_row_index_list):
        item_row_index_list[0] = update_item_index(item_row_index_list[0], 1)
        update_item_label(items_df, item_row_index_list[0])

    def confirm_barcode_input(item_row_index_list):
        selected_items = get_selected_items(items_df)
        item_row_index_list[0] = 0
        if len(selected_items) > 0:
            if len(selected_items) > 1:
                left_arrow_button.configure(state="normal")
                right_arrow_button.configure(state="normal")
            update_item_label(items_df, item_row_index_list[0])
            confirm_button.configure(state="normal")
        else:
            reset_form()

    def confirm_input():
        selected_items = get_selected_items(items_df)
        remove_item(
            items_df, selected_items.iloc[selected_item_index].index, int(quantity_entry.get()))

        # Clear the entries for the next input
        reset_form()

    def cancel_input():
        ai_window.destroy()

    barcode_frame = ctk.CTkFrame(ai_window)
    barcode_frame.pack(pady=10)
    barcode_label = ctk.CTkLabel(
        barcode_frame, text="Barcode:", width=label_width, height=label_height, font=label_font)
    barcode_label.pack(side=ctk.LEFT, padx=10)
    barcode_entry = ctk.CTkEntry(
        barcode_frame, width=input_width, height=input_height, font=input_font)
    barcode_entry.bind("<Key>", lambda event: on_barcode_change(
        event=event, item_row_index_list=selected_item_index))
    barcode_entry.focus()
    barcode_entry.pack(side=ctk.LEFT)

    right_arrow_button = ctk.CTkButton(barcode_frame, text="▶", command=lambda: move_right(
        item_row_index_list=selected_item_index), font=button_font, height=button_height, width=button_height)
    left_arrow_button = ctk.CTkButton(barcode_frame, text="◀", command=lambda: move_left(
        item_row_index_list=selected_item_index), font=button_font, height=button_height, width=button_height)

    right_arrow_button.pack(side=ctk.RIGHT)
    left_arrow_button.pack(side=ctk.RIGHT, padx=10)

    # Item details frame
    label_frame = ctk.CTkFrame(ai_window, width=890, height=200)
    label_frame.pack(pady=10)
    label = ctk.CTkLabel(label_frame, text="",
                         font=label_font, width=890, height=200)
    label.pack(side=ctk.RIGHT)

    # Quantity frame + and - buttons
    quantity_frame = ctk.CTkFrame(ai_window, width=890, height=200)
    quantity_frame.pack(pady=10)
    quantity_label = ctk.CTkLabel(
        quantity_frame, text="Quantity:", width=label_width, height=label_height, font=label_font)
    quantity_label.pack(side=ctk.LEFT, padx=(0, 10))
    quantity_entry = ctk.StringVar(value="1")
    quantity_label_value = ctk.CTkLabel(
        quantity_frame, textvariable=quantity_entry, width=label_width, height=label_height, font=input_font)
    quantity_label_value.pack(side=ctk.LEFT, padx=10)

    def update_quantity(value):
        current_value = float(quantity_entry.get())
        new_value = max(1, current_value + value)
        quantity_entry.set(f"{new_value:.0f}")

    plus_button = ctk.CTkButton(
        quantity_frame, text="+", command=lambda: update_quantity(1.0), font=input_font, height=button_height, width=button_height)
    plus_button.pack(side=ctk.LEFT)

    minus_button = ctk.CTkButton(
        quantity_frame, text="-", command=lambda: update_quantity(-1.0), font=input_font, height=button_height, width=button_height)
    minus_button.pack(side=ctk.LEFT, padx=(10, 0))

    # Create Confirm and Cancel buttons side by side
    button_frame = ctk.CTkFrame(ai_window)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_input,
                                  width=button_width, height=button_height, font=button_font)
    cancel_button.pack(side=ctk.LEFT, padx=(0, 10))

    confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=confirm_input,
                                   width=button_width, height=button_height, font=button_font)
    confirm_button.configure(state="disabled")
    confirm_button.pack(side=ctk.LEFT)

    # Pack the canvas
    canvas.pack()
