from openfoodfacts_connector import get_desc_from_barcode

def find_desc_from_barcode(barcode):
    description = get_desc_from_barcode(barcode)
    return description
