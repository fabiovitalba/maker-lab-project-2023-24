from datetime import datetime
import pandas as pd
from tabulate import tabulate

from adafruit_connector import read_items, add_item, reduce_item
from openfoodfacts_connector import get_desc_from_barcode


def get_expiration_date():
    while True:
        expiration_date_str = input("Enter expiration date (DD/MM/YYYY): ")
        try:
            expiration_date = datetime.strptime(
                expiration_date_str, '%d/%m/%Y')
            return expiration_date
        except ValueError:
            print("\033[33mInvalid date format. Please try again.\033[0m")


def get_quantity(str):
    while True:
        try:
            quantity = int(input(str))
            return quantity
        except ValueError:
            print("\033[33mInvalid input. Please enter a number.\033[0m")


def colorize_rows(df):
    df = df.astype(str)
    for i in range(len(df)):
        # Parse the date string into a datetime object
        date = datetime.strptime(df.loc[i, 'Expiration Date'], '%d/%m/%Y')

        # Get the current date
        now = datetime.now()

        # Calculate the difference between the date and now
        diff = (date - now).days

        # Colorize based on the difference
        if diff <= 1:
            df.loc[i] = '\033[31m' + df.loc[i].astype(str) + '\033[0m'  # red
        elif diff <= 3:
            df.loc[i] = '\033[33m' + \
                df.loc[i].astype(str) + '\033[0m'  # yellow

    return df


def main():

    print("\n" + "*" * 42)
    print("*" + "Fridge Inventory Management".center(40) + "*")
    print("+" + "D. Di Bella & F. Vitalba".center(40) + "*")
    print("*" * 42 + "\n")
    items_df = read_items()

    try:
        while True:

            print("Please choose an option:")
            print("\033[1mL\033[0m: List all items")
            print("\033[1mA\033[0m: Add an item")
            print("\033[1mR\033[0m: Remove an item")
            print("\033[1mQ\033[0m: Quit")
            option = input("Your option: ").upper()

            if option == 'L':
                if (len(items_df) <= 0):
                    print("\033[33mNo items found.\033[0m\n")
                    continue

                print(items_df)
                continue

                # Print items in a formatted table
                items_copy = items_df.copy()
                items_copy['Timestamp'] = pd.to_datetime(
                    items_copy['Timestamp']).dt.strftime('%d/%m/%Y')
                items_copy['Expiration Date'] = pd.to_datetime(
                    items_copy['Expiration Date'], unit='ms').dt.strftime('%d/%m/%Y')
                items_copy['Date added'] = pd.to_datetime(
                    items_copy['Date added'], unit='ms').dt.strftime('%d/%m/%Y')
                items_copy['Date modified'] = pd.to_datetime(
                    items_copy['Date modified'], unit='ms').dt.strftime('%d/%m/%Y')
                items_copy.sort_values(by=['Expiration Date'], inplace=True)
                items_copy = colorize_rows(items_copy)
                headers = [header.upper() for header in items_copy.columns]
                print(tabulate(items_copy, headers=headers,
                      tablefmt='fancy_grid', showindex=False, colalign=("center",)*len(headers)))

            elif option == 'A':
                barcode = input("Enter barcode: ")
                description_temp = get_desc_from_barcode(barcode)
                if (description_temp != ''):
                    description = input(
                        f"Enter name (press enter for '{description_temp}'): ") or description_temp
                else:
                    description = input("Enter name: ")
                quantity = get_quantity("Enter quantity: ")
                expiration_date = get_expiration_date()
                new_item = [datetime.now(), barcode, description, expiration_date,
                            quantity, datetime.now(), None]
                if not add_item(items_df, new_item):
                    print('\033[31mADD_ITEM-method FAILED\033[0m')
                else:
                    print('\033[92mItem added successfully\033[0m')

            elif option == 'R':
                barcode = input("Enter barcode: ")
                quantity = get_quantity("Enter quantity (0 to remove all): ")
                reduce_item(items_df, barcode, quantity)

            elif option == 'Q':
                print("\nProgram terminated by user. Goodbye!")
                break

            else:
                print("\033[93mInvalid option. Please try again.\033[0m")

            print("")
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")


if __name__ == "__main__":
    main()
