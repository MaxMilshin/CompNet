import requests

BASE_URL = 'http://localhost:5000'

# Get all products
response = requests.get(BASE_URL + '/products')
if response.status_code == 200:
    products = response.json()
    print(f"All products: {products}")
else:
    print(f"Error: {response.status_code} - {response.json()}")

# Get product by ID
product_id = 1
response = requests.get(BASE_URL + f'/products/{product_id}')
if response.status_code == 200:
    product = response.json()
    print(f"Product with ID {product_id}: {product}")
else:
    print(f"Error: {response.status_code} - {response.json()}")

# Add new product
new_product = {
    "name": "Nike LeBron 20", 
    "description": "There was no doubt that Nike would go all out for LeBron James' 20th signature sneaker. After a lull in recent years, James' shoes are back and better than ever, thanks to its new slimmed-down silhouette.",
    "icon": "https://www.si.com/.image/c_limit%2Ccs_srgb%2Cq_auto:good%2Cw_700/MTkzMjEwNDg3MDU4NDc0OTE1/usatsi_19186924.webp"
}
response = requests.post(BASE_URL + '/products', json=new_product)
if response.status_code == 201:
    product = response.json()
    print(f"New product added with ID {product['id']}: {product}")
else:
    print(f"Error: {response.status_code} - {response.json()}")

# Update product info
product_id = 1
updated_product = {
    "name": "New Balance TWO WXY v3", 
    "description": "New Balance grabbed headlines at the 2022 NBA Media Day thanks to an unreleased shoe worn by its roster of signature athletes. We later learned the players wore the New Balance TWO WXY v3.",
    "icon": "https://www.si.com/.image/c_limit%2Ccs_srgb%2Cq_auto:good%2Cw_700/MTk0NDE2NTU1MjE0MjUxNTI1/usatsi_19173688.webp"
}
response = requests.put(BASE_URL + f'/products/{product_id}', json=updated_product)
if response.status_code == 200:
    product = response.json()
    print(f"Product with ID {product_id} updated: {product}")
else:
    print(f"Error: {response.status_code} - {response.json()}")

# Delete product by ID
product_id = 2
response = requests.delete(BASE_URL + f'/products/{product_id}')
if response.status_code == 200:
    print(f"Product with ID {product_id} deleted")
else:
    print(f"Error: {response.status_code} - {response.json()}")
