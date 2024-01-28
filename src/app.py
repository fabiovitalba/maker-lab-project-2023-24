from datetime import datetime
import pandas as pd
from tabulate import tabulate

from adafruit_connector import read_items, add_item, reduce_item
from openfoodfacts_connector import get_desc_from_barcode


def get_expiration_date():
    while True:
        expiration_date_str = input("Enter expiration date (DD/MM/YYYY): ")
        try:
            expiration_date = pd.to_datetime(expiration_date_str).timestamp()
            return expiration_date
        except ValueError:
            print("\033[33mInvalid date format. Please try again.\033[0m")


def get_quantity(str):
    while True:
        try:
            quantity = int(input(str) or (1))
            return quantity
        except ValueError:
            print("\033[33mInvalid input. Please enter a number.\033[0m")


def colorize_rows(df):
    
    for i in range(len(df)):

        # Get the current date
        now = datetime.now()

        # Calculate the difference between the date and now
        diff = (df.loc[i, "Expiration Date"] - now).days

        print(df.loc[i, "Expiration Date"].strftime("%B %d, %Y"))

        df.loc[i, "Expiration Date"] = df.loc[i, "Expiration Date"].strftime("%B %d, %Y")
        df.loc[i, "Date added"] = df.loc[i, "Date added"].strftime("%B %d, %Y")

        print(df.loc[i, "Date added"])

        df.loc[i] = df.loc[i].astype(str)
        
        # Colorize based on the difference
        if diff <= 1:
            df.loc[i] = "\033[31m" + df.loc[i].astype(str) + "\033[0m"  # red
        elif diff <= 3:
            df.loc[i] = "\033[33m" + \
                df.loc[i].astype(str) + "\033[0m"  # yellow

    return df


def main():

    print("\n" + "*" * 42)
    print("*" + "Fridge Inventory Management".center(40) + "*")
    print("*" + "D. Di Bella & F. Vitalba".center(40) + "*")
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

            if option == "L":
                if (len(items_df) <= 0):
                    print("\033[33mNo items found.\033[0m\n")
                    continue

                # uncomment to skip formatted printing
                
                #items_copy = items_df.copy()
                #print(items_df)
                #continue

                # Print items in a formatted table
                items_copy = items_df.copy()
                items_copy.sort_values(by=["Expiration Date"], inplace=True)
                items_copy["Expiration Date"] = pd.to_datetime(items_copy["Expiration Date"], unit="s")
                items_copy["Date added"] = pd.to_datetime(items_copy["Date added"], unit="s")
                items_copy["Date modified"] = pd.to_datetime(items_copy["Date modified"], unit="s")
                items_copy = colorize_rows(items_copy)
                headers = [header.upper() for header in items_copy.columns]
                print(tabulate(items_copy, headers=headers,
                      tablefmt="fancy_grid", showindex=False, colalign=("center",)*len(headers)))

            elif option == "A":
                barcode = input("Enter barcode: ")
                description_temp = get_desc_from_barcode(barcode)
                if (description_temp != ""):
                    description = input(f"Enter name (press enter for '{description_temp}'): ") or description_temp
                else:
                    description = input("Enter name: ")
                quantity = get_quantity("Enter quantity (press enter for 1): ")
                expiration_date = get_expiration_date()
                new_item = [barcode, description, expiration_date,
                            quantity, pd.to_datetime("now").timestamp(), None]
                if not add_item(items_df, new_item):
                    print("\033[31mCould not add item.\033[0m")
                else:
                    print("\033[92mItem added successfully!\033[0m")

            elif option == "R":
                # continue reading for barcode until one that is in items_df is provided
                while True:
                    barcode = input("Enter a barcode: ")
                    if barcode in items_df["Barcode"].values:
                        break
                    else:
                        print(
                            "\033[93mBarcode not found. Please try again.\033[0m")

                quantity = get_quantity("Enter quantity to remove (press enter for 1): ")
                reduce_item(items_df, barcode, quantity)

            elif option == "Q":
                print("\nProgram terminated by user. Goodbye!")
                break

            else:
                print("\033[93mInvalid option. Please try again.\033[0m")

            print()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")


if __name__ == "__main__":
    main()
