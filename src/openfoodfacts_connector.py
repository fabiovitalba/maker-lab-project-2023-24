import requests


# Receives a barcode string and returns a description found on the openfoodfacts API. If no
# description is found, an empty string is returned.
def get_desc_from_barcode(barcode):
    # The page https://world.openfoodfacts.org/data provides free data connected to the provided barcode.
    # Using this URL we can retrieve the description of the product using only the barcode.

    # Using this https://world.openfoodfacts.org/api/v2/product/[barcode].json we retrieve the data starting from a barcode.
    request_url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(request_url)

    if 200 <= response.status_code < 400:
        data = response.json()
        if "product" in data:
            if "product_name" in data["product"]:
                return data["product"]["product_name"]
        return ""
    else:
        return ""
