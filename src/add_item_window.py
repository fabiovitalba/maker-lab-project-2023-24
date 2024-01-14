import customtkinter as ctk
from CTkTable import *

def add_item_window(win_height, win_width, button_font, items_df):
    ai_window = ctk.CTkToplevel()
    canvas = ctk.CTkCanvas(ai_window, height=win_height, width=win_width)

    button_width = 450
    button_height = 100
    label_font = ("Helvetica", 20)
    label_width = 450
    label_height = 100
    input_font = ("Helvetica", 20, "bold")
    input_width = 450
    input_height = 100

    def on_barcode_change(event):
        print(barcode_entry.get())

    def on_description_change(event):
        print(description_entry.get())

    def on_quantity_change(event):
        print(quantity_entry.get())

    def on_exp_date_change(event):
        print(expiration_date_entry.get())

    def confirm_input():
        barcode_value = barcode_entry.get()
        description_value = description_entry.get()
        quantity_value = quantity_entry.get()
        expiration_date_value = expiration_date_entry.get()

        # You can process the input values as needed
        print("Barcode:", barcode_value)
        print("Description:", description_value)
        print("Quantity:", quantity_value)
        print("Expiration Date:", expiration_date_value)

        # Add your logic to handle the confirmed input

        # Clear the entries for the next input
        barcode_entry.delete(0, ctk.END)
        description_entry.delete(0, ctk.END)
        quantity_entry.delete(0, ctk.END)
        expiration_date_entry.delete(0, ctk.END)

    def cancel_input():
        ai_window.destroy()

    # Create and pack the input labels and entry widgets
    barcode_frame = ctk.CTkFrame(ai_window)
    barcode_frame.pack(pady=10)
    barcode_label = ctk.CTkLabel(barcode_frame, text="Barcode:", width=label_width, height=label_height, font=label_font)
    barcode_label.pack(side=ctk.LEFT, padx=10)
    barcode_entry = ctk.CTkEntry(barcode_frame, width=input_width, height=input_height, font=input_font)
    barcode_entry.bind("<Key>", on_barcode_change)
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
    quantity_label.pack(side=ctk.LEFT, padx=10)
    quantity_entry = ctk.CTkEntry(quantity_frame, width=input_width, height=input_height, font=input_font)
    quantity_entry.bind("<Key>", on_quantity_change)
    quantity_entry.pack(side=ctk.LEFT)

    expiration_date_frame = ctk.CTkFrame(ai_window)
    expiration_date_frame.pack(pady=10)
    expiration_date_label = ctk.CTkLabel(expiration_date_frame, text="Expiration Date:", width=label_width, height=label_height, font=label_font)
    expiration_date_label.pack(side=ctk.LEFT, padx=10)
    expiration_date_entry = ctk.CTkEntry(expiration_date_frame, width=input_width, height=input_height, font=input_font)
    expiration_date_entry.bind("<Key>", on_exp_date_change)
    expiration_date_entry.pack(side=ctk.LEFT)

    # Create Confirm and Cancel buttons side by side
    button_frame = ctk.CTkFrame(ai_window)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_input, width=button_width, height=button_height, font=button_font)
    cancel_button.pack(side=ctk.LEFT, padx=10)

    confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=confirm_input, width=button_width, height=button_height, font=button_font)
    confirm_button.pack(side=ctk.LEFT)

    # Pack the canvas
    canvas.pack()
