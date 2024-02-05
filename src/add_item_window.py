import customtkinter as ctk
import pandas as pd
import datetime

from item import find_desc_from_barcode
from adafruit_connector import add_item
from expiration_date import handle_exp_date_input


def add_item_window(win_height, win_width, button_font, items_df):
    ai_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(ai_window, height=win_height, width=win_width)

    button_width = 450
    button_height = 100
    label_font = ("Helvetica", 20)
    label_width = 300
    label_height = 100
    input_font = ("Helvetica", 20, "bold")
    input_width = 600
    input_height = 100
    # This must be a list in order to be mutable from the change_event
    curr_exp_date_list = [datetime.date.today()]

    def reset_form():
        barcode_entry.delete(0, ctk.END)
        description_entry.delete(0, ctk.END)
        expiration_date_entry.delete(0, ctk.END)
        curr_exp_date_list[0] = datetime.date.today()
        barcode_entry.focus()
        confirm_button.configure(state="disabled")

    def focus_expiration_date_input():
        expiration_date_entry.delete(0, ctk.END)
        expiration_date_entry.insert(0, str(curr_exp_date_list[0].strftime("%d/%m/%Y")))
        expiration_date_entry.focus()
        confirm_button.configure(state="normal")

    def on_barcode_change(event):
        barcode = barcode_entry.get()
        if (event.keysym == "Return") and (barcode != ""):
            description = find_desc_from_barcode(barcode)
            if description == "":
                # jump to description
                description_entry.focus()
            else:
                # Set the description and jump to expiration date input
                description_entry.delete(0, ctk.END)
                description_entry.insert(0, description)
                focus_expiration_date_input()

    def on_description_change(event):
        if event.keysym == "Return":
            description = description_entry.get()
            if description != "":
                focus_expiration_date_input()

    def on_exp_date_change(event, exp_date_list):
        exp_date_text = expiration_date_entry.get()
        next_input = False
        if event.keysym == "Return":
            [exp_date_list[0], next_input] = handle_exp_date_input(exp_date_text, exp_date_list[0])
            if next_input:
                confirm_input()
            else:
                focus_expiration_date_input()

    def confirm_input():
        confirm_button.configure(state="disabled")
        barcode_value = barcode_entry.get()
        description_value = description_entry.get()
        quantity_value = quantity_entry.get()

        # You can process the input values as needed
        new_item = [barcode_value, description_value, pd.to_datetime(curr_exp_date_list[0]).timestamp(), quantity_value, pd.to_datetime("now").timestamp()]
        add_item(items_df, new_item)

        # Clear the entries for the next item input
        reset_form()

    def cancel_input():
        ai_window.destroy()

    def update_quantity(value):
        current_value = float(quantity_entry.get())
        new_value = max(1, current_value + value)
        quantity_entry.set(f"{new_value:.0f}")

    # Create and pack the input labels and entry widgets
    barcode_frame = ctk.CTkFrame(ai_window)
    barcode_frame.pack(pady=10)
    barcode_label = ctk.CTkLabel(barcode_frame, text="Barcode:", width=label_width, height=label_height, font=label_font)
    barcode_label.pack(side=ctk.LEFT, padx=10)
    barcode_entry = ctk.CTkEntry(barcode_frame, width=input_width, height=input_height, font=input_font)
    barcode_entry.bind("<Key>", on_barcode_change)
    barcode_entry.focus()
    barcode_entry.pack(side=ctk.LEFT)

    description_frame = ctk.CTkFrame(ai_window)
    description_frame.pack(pady=10)
    description_label = ctk.CTkLabel(description_frame, text="Description:", width=label_width, height=label_height, font=label_font)
    description_label.pack(side=ctk.LEFT, padx=10)
    description_entry = ctk.CTkEntry(description_frame, width=input_width, height=input_height, font=input_font)
    description_entry.bind("<Key>", on_description_change)
    description_entry.pack()

    quantity_frame = ctk.CTkFrame(ai_window)
    quantity_frame.pack(pady=10)
    quantity_label = ctk.CTkLabel(quantity_frame, text="Quantity:", width=label_width, height=label_height, font=label_font)
    quantity_label.pack(side=ctk.LEFT, padx=(0, 10))
    quantity_entry = ctk.StringVar(value="1")
    quantity_label_value = ctk.CTkLabel(quantity_frame, textvariable=quantity_entry, width=label_width, height=label_height, font=input_font)
    quantity_label_value.pack(side=ctk.LEFT, padx=10)
    plus_button = ctk.CTkButton(quantity_frame, text="+", command=lambda: update_quantity(1.0), font=input_font, height=button_height)
    plus_button.pack(side=ctk.LEFT)
    minus_button = ctk.CTkButton(quantity_frame, text="-", command=lambda: update_quantity(-1.0), font=input_font,  height=button_height)
    minus_button.pack(side=ctk.LEFT, padx=(10, 0))

    expiration_date_frame = ctk.CTkFrame(ai_window)
    expiration_date_frame.pack(pady=10)
    expiration_date_label = ctk.CTkLabel(expiration_date_frame, text="Expiration Date (dd/mm/yyyy):", width=label_width, height=label_height, font=label_font)
    expiration_date_label.pack(side=ctk.LEFT, padx=10)
    expiration_date_entry = ctk.CTkEntry(expiration_date_frame, width=input_width, height=input_height, font=input_font)
    expiration_date_entry.bind("<Key>", lambda event: on_exp_date_change(event=event, exp_date_list=curr_exp_date_list))
    expiration_date_entry.pack(side=ctk.LEFT)

    # Create Confirm and Cancel buttons side by side
    button_frame = ctk.CTkFrame(ai_window)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_input, width=button_width, height=button_height, font=button_font)
    cancel_button.pack(side=ctk.LEFT, padx=(0, 10))

    confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=confirm_input, width=button_width, height=button_height, font=button_font)
    confirm_button.configure(state="disabled")
    confirm_button.pack(side=ctk.LEFT)

    # Pack the canvas
    canvas.pack()
