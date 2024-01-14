import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk

def list_items(inventory):
    display_message("List of Items:\n" + "\n".join(inventory))

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
    message_label = tk.Label(root, text=message)
    message_label.pack(pady=10)
    # Auto-remove the message after a few seconds
    root.after(3000, message_label.destroy)

def main():
    root = ctk.CTk()
    root.title("Fridge Inventory Management")
    root.geometry("1024x600")
    button_font = ("Helvetica", 28, "bold")

    inventory = []

    # Create a label for the title
    title_label = tk.Label(root, text="Fridge Inventory Management\nD. di Bella & F. Vitalba", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=20)

    # Create a button for each option with larger size
    button_width = 90
    button_height = 3

    list_button = tk.Button(root, text="List all items", command=lambda: list_items(inventory), width=button_width, height=button_height, font=button_font)
    list_button.pack(pady=10)

    add_button = tk.Button(root, text="Add an item", command=lambda: add_item(inventory), width=button_width, height=button_height, font=button_font)
    add_button.pack(pady=10)

    remove_button = tk.Button(root, text="Remove an item", command=lambda: remove_item(inventory), width=button_width, height=button_height, font=button_font)
    remove_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.destroy, width=button_width, height=button_height, font=button_font)
    quit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
