from PIL import Image, ImageDraw 

import math 

 

# Create the image canvas 

img = Image.new('RGB', (1000, 1000), 'white') 

draw = ImageDraw.Draw(img) 

 

# Draw the house body 

draw.polygon(((100, 500), (800, 500), (800, 800), (100, 800)), outline='black', fill='orange') 

 

# Draw the door 

draw.polygon(((400, 600), (500, 600), (500, 800), (400, 800)), outline='black', fill='brown') 

 

# Draw the windows 

draw.polygon(((200, 600), (300, 600), (300, 700), (200, 700)), outline='black', fill='blue') 

draw.polygon(((600, 600), (700, 600), (700, 700), (600, 700)), outline='black', fill='blue') 

 

# Draw the arc (cord) as a roof 

# Define the bounding box for the arc (cord) 

left = 100  # Left coordinate of the bounding box 

top = 100   # Top coordinate of the bounding box 

right = 800  # Right coordinate of the bounding box 

bottom = 500  # Bottom coordinate of the bounding box 

 

# Draw an arc for the roof between 0 to 180 degrees 

draw.arc((left, top, right, bottom), start=0, end=180, fill='black', width=5) 

 

# Display the image 

img.show() 
