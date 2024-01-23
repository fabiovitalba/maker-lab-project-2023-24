import customtkinter as ctk

def remove_item_window(win_height, win_width, button_font, items_df):
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

    def on_barcode_change(event):
        barcode = barcode_entry.get()
        if event.keysym == "Return":
            print("confirm")

    def move_left():
        #TODO: implement previous function for selected items
        pass

    def move_right():
        #TODO: implement next function for selected items
        pass

    def confirm_input():
        barcode_value = barcode_entry.get()

        # You can process the input values as needed

        # Clear the entries for the next input
        barcode_entry.delete(0, ctk.END)
        barcode_entry.focus()

    def cancel_input():
        ai_window.destroy()

    barcode_frame = ctk.CTkFrame(ai_window)
    barcode_frame.pack(pady=10)
    barcode_label = ctk.CTkLabel(barcode_frame, text="Barcode:", width=label_width, height=label_height, font=label_font)
    barcode_label.pack(side=ctk.LEFT, padx=10)
    barcode_entry = ctk.CTkEntry(barcode_frame, width=input_width, height=input_height, font=input_font)
    barcode_entry.bind("<Key>", on_barcode_change)
    barcode_entry.focus()
    barcode_entry.pack(side=ctk.LEFT)

    label_frame = ctk.CTkFrame(ai_window, width=890, height=200)
    label_frame.pack(pady=10)
    #TODO: write selected items text in label.
    label = ctk.CTkLabel(label_frame, text="Label Text", font=label_font, width=700, height=200)
    label.pack(side=ctk.RIGHT)

    arrow_frame = ctk.CTkFrame(label_frame, width=50)
    arrow_frame.pack(side=ctk.RIGHT)
    right_arrow_button = ctk.CTkButton(arrow_frame, text="▶", command=move_right, font=button_font, height=button_height, width=button_height)
    right_arrow_button.configure(state="disabled")
    left_arrow_button = ctk.CTkButton(arrow_frame, text="◀", command=move_left, font=button_font, height=button_height, width=button_height)
    left_arrow_button.configure(state="disabled")  #use "normal" to enable the buttons

    right_arrow_button.pack(side=ctk.RIGHT, padx=10)
    left_arrow_button.pack(side=ctk.RIGHT)

    # Create Confirm and Cancel buttons side by side
    button_frame = ctk.CTkFrame(ai_window)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_input, width=button_width, height=button_height, font=button_font)
    cancel_button.pack(side=ctk.LEFT, padx=10)

    confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=confirm_input, width=button_width, height=button_height, font=button_font)
    confirm_button.pack(side=ctk.LEFT)

    # Pack the canvas
    canvas.pack()
