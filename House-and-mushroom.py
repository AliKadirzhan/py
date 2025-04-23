from PIL import Image, ImageDraw 
import matplotlib.pyplot as plt 
import math 
 
img = Image.new('RGB', (2000, 1000), 'white') 
draw = ImageDraw.Draw(img) 
 
 
draw.polygon(((100, 500), (800, 500), (800, 800), (100, 800)), outline='black', fill='orange') 
draw.polygon(((400, 600), (500, 600), (500, 800), (400, 800)), outline='black', fill='brown') 
draw.polygon(((50, 500), (450, 200), (850, 500)), outline='black', fill='red') 
draw.polygon(((200, 600), (300, 600), (300, 700), (200, 700)), outline='black', fill='blue') 
draw.polygon(((600, 600), (700, 600), (700, 700), (600, 700)), outline='black', fill='blue') 
 
draw.pieslice([1200, 300, 1800, 700], start=180, end=360, fill='red', outline='black') 
draw.rectangle((1450, 500, 1550, 800), fill=(210, 180, 140), outline="black") 
 
img.show() 
 
plt.imshow(img) 
plt.axis('on') 
plt.grid(True) 
plt.show() 
