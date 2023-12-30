from openfoodfacts_connector import get_desc_from_barcode

olives_description = get_desc_from_barcode('8056149086957') # S-Budget Olive Nere Denocciolate in Salamoia
print(olives_description)

mayo_description = get_desc_from_barcode('8001300242802') # Maionese vegetale
print(mayo_description)
