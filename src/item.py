from openfoodfacts_connector import get_desc_from_barcode


# Receives a barcode string and returns the description found using that barcode. If no
# description is found, an empty string is returned.
def find_desc_from_barcode(barcode):
    description = get_desc_from_barcode(barcode)
    return description
