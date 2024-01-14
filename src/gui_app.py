import customtkinter as ctk
from tkinter import simpledialog
from item_list_window import item_list_window

from adafruit_connector import read_items

WIN_WIDTH = 1024
WIN_HEIGHT = 600
TITLE_FONT = ("Helvetica", 18, "bold")
BUTTON_FONT = ("Helvetica", 28, "bold")

def add_item(inventory):
    item = simpledialog.askstring("Add Item", "Enter the item:")
    if item:
        inventory.append(item)
        display_message(f"Item '{item}' added successfully.")

def remove_item(inventory):
    item = simpledialog.askstring("Remove Item", "Enter the item to remove:")
    if item in inventory:
        inventory.remove(item)
        display_message(f"Item '{item}' removed successfully.")
    else:
        display_message(f"Item '{item}' not found.")

def display_message(message):
    print(message)
    #message_label = tk.Label(root, text=message)
    #message_label.pack(pady=10)
    # Auto-remove the message after a few seconds
    #root.after(3000, message_label.destroy)

def main_menu_window(mm_window, items_df):
    canvas = ctk.CTkCanvas(mm_window, height=WIN_HEIGHT, width=WIN_WIDTH)
    title_label = ctk.CTkLabel(mm_window, text="Fridge Inventory Management")
    title_label.pack(pady=2)
    window_subtitle = ctk.CTkLabel(mm_window, text="D. Di Bella & F. Vitalba")
    window_subtitle.pack(pady=2)

    button_width = 900
    button_height = 100

    list_button = ctk.CTkButton(mm_window, text="List all items", command=lambda: item_list_window(WIN_HEIGHT, WIN_WIDTH, BUTTON_FONT, items_df), width=button_width, height=button_height, font=BUTTON_FONT)
    list_button.pack(pady=10)
    add_button = ctk.CTkButton(mm_window, text="Add an item", command=lambda: add_item(), width=button_width, height=button_height, font=BUTTON_FONT)
    add_button.pack(pady=10)
    remove_button = ctk.CTkButton(mm_window, text="Remove an item", command=lambda: remove_item(), width=button_width, height=button_height, font=BUTTON_FONT)
    remove_button.pack(pady=10)
    quit_button = ctk.CTkButton(mm_window, text="Quit", command=mm_window.destroy, width=button_width, height=button_height, font=BUTTON_FONT)
    quit_button.pack(pady=10)
    canvas.pack()

def main():
    ctk.set_appearance_mode("dark")
    window = ctk.CTk()
    window.title("Fridge Inventory Management")
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    window.resizable(False, False)

    items_df = read_items()
    print(items_df)
    main_menu_window(window, items_df)
    window.mainloop()

if __name__ == "__main__":
    main()
