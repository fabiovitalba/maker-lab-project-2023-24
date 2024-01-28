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
    selected_item_index = [0]

    def reset_form():
        left_arrow_button.configure(state="disabled")
        right_arrow_button.configure(state="disabled")
        confirm_button.configure(state="disabled")
        label.configure(text="")
        barcode_entry.delete(0, ctk.END)
        barcode_entry.focus()

    def on_barcode_change(event, item_row_index_list):
        barcode = barcode_entry.get()
        if event.keysym == "Return":
            confirm_barcode_input(item_row_index_list)

    def update_item_label(items_df, item_row_index):
        barcode_value = barcode_entry.get()
        selected_items = items_df.loc[items_df['Barcode'] == barcode_value]
        # TODO: Add information about expiration date
        label.configure(text=f"{selected_items.iloc[item_row_index]['Description']} ({selected_items.iloc[item_row_index]['Quantity']})")

    def update_item_index(index, delta):
        barcode_value = barcode_entry.get()
        selected_items = items_df.loc[items_df['Barcode'] == barcode_value]
        if index + delta < 0:
            index = len(selected_items) - 1
        elif index + delta >= len(selected_items):
            index = 0
        else:
            index = index + delta
        return index

    def move_left(item_row_index_list):
        print(item_row_index_list)
        item_row_index_list[0] = update_item_index(item_row_index_list[0], -1)
        print(item_row_index_list)
        update_item_label(items_df,item_row_index_list[0])

    def move_right(item_row_index_list):
        print(item_row_index_list)
        item_row_index_list[0] = update_item_index(item_row_index_list[0], 1)
        print(item_row_index_list)
        update_item_label(items_df,item_row_index_list[0])

    def confirm_barcode_input(item_row_index_list):
        barcode_value = barcode_entry.get()
        print(items_df)
        item_row_index_list[0] = 0
        selected_items = items_df.loc[items_df['Barcode'] == barcode_value]
        if len(selected_items) > 0:
            if len(selected_items) > 1:
                left_arrow_button.configure(state="normal")
                right_arrow_button.configure(state="normal")
            update_item_label(items_df,item_row_index_list[0])
            confirm_button.configure(state="normal")
        else:
            reset_form()

    def confirm_input():
        barcode_value = barcode_entry.get()

        # You can process the input values as needed

        # Clear the entries for the next input
        reset_form()

    def cancel_input():
        ai_window.destroy()

    barcode_frame = ctk.CTkFrame(ai_window)
    barcode_frame.pack(pady=10)
    barcode_label = ctk.CTkLabel(barcode_frame, text="Barcode:", width=label_width, height=label_height, font=label_font)
    barcode_label.pack(side=ctk.LEFT, padx=10)
    barcode_entry = ctk.CTkEntry(barcode_frame, width=input_width, height=input_height, font=input_font)
    barcode_entry.bind("<Key>", lambda event: on_barcode_change(event=event, item_row_index_list=selected_item_index))
    barcode_entry.focus()
    barcode_entry.pack(side=ctk.LEFT)

    label_frame = ctk.CTkFrame(ai_window, width=890, height=200)
    label_frame.pack(pady=10)
    label = ctk.CTkLabel(label_frame, text="", font=label_font, width=700, height=200)
    label.pack(side=ctk.RIGHT)

    arrow_frame = ctk.CTkFrame(label_frame, width=50)
    arrow_frame.pack(side=ctk.RIGHT)
    right_arrow_button = ctk.CTkButton(arrow_frame, text="▶", command=lambda: move_right(item_row_index_list=selected_item_index), font=button_font, height=button_height, width=button_height)
    right_arrow_button.configure(state="disabled")
    left_arrow_button = ctk.CTkButton(arrow_frame, text="◀", command=lambda: move_left(item_row_index_list=selected_item_index), font=button_font, height=button_height, width=button_height)
    left_arrow_button.configure(state="disabled")

    right_arrow_button.pack(side=ctk.RIGHT, padx=10)
    left_arrow_button.pack(side=ctk.RIGHT)

    # Create Confirm and Cancel buttons side by side
    button_frame = ctk.CTkFrame(ai_window)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_input, width=button_width, height=button_height, font=button_font)
    cancel_button.pack(side=ctk.LEFT, padx=10)

    confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=confirm_input, width=button_width, height=button_height, font=button_font)
    confirm_button.configure(state="disabled")
    confirm_button.pack(side=ctk.LEFT)

    # Pack the canvas
    canvas.pack()
