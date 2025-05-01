#pip install Pillow
#pip install qrcode
#pip install reportlab
#source ~/py_envs/bin/activate

import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, LETTER, landscape

import os
import sys

pdf_path = "output.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)

page_width, page_height = A4

# Define grid dimensions (rows × columns)
rows, cols = 8, 6  

margin_x = 50
margin_y = 50  # Left, Right, Top, Bottom margins

usable_width = page_width - (2 * margin_x)
usable_height = page_height - (2 * margin_y)

cell_width = usable_width / cols
cell_height = usable_height / rows

image_size = 72  # Set image size (width & height)
image_width = 72
image_height = 72

border_padding = 10  # Additional space around each image

for row in range(rows + 1):
    y = page_height - margin_y - (row * cell_height)
    c.line(margin_x, y, margin_x + usable_width, y)  # Horizontal line

for col in range(cols + 1):
    x = margin_x + (col * cell_width)
    c.line(x, page_height - margin_y, x, page_height - margin_y - usable_height)  # Vertical line

i = 0
# Draw the grid
for row in range(rows + 1):
    for col in range(cols + 1):

        # Data to be encoded
        data = f"http://10.0.0.147:8001/items/{i}/details"

        i = i + 1

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        img = qr.make_image(fill_color="black", back_color="white")
        image_path = f"{i}simple_qrcode.png"
        
        # Save the image
        img.save(image_path)
        
        x = margin_x + (col * cell_width) - (image_width / 2)  # Center images on intersection
        y = page_height - margin_y - (row * cell_height) - (image_height / 2)

        # Draw image at the intersection point
        c.drawImage(image_path, x, y, width=image_width, height=image_height)

        os.remove(image_path)
        

c.save()