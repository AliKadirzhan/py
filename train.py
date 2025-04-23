from PIL import Image, ImageDraw 
 
img = Image.new('RGB', (1200, 1000), 'white') 
draw = ImageDraw.Draw(img) 
 
draw.rectangle((100, 250, 1000, 400), fill='darkred', outline='black', width=5) 
 
draw.rectangle((800, 150, 1000, 250), fill='darkgray', outline='black', width=5) 
 
 
 
draw.rectangle((850, 270, 950, 320), fill='lightgray', outline='black', width=3) 
 
wheel_radius = 50 
wheel_spacing = 180 
 
for i in range(5): 
    draw.ellipse((190 + i * wheel_spacing - wheel_radius, 400 - wheel_radius, 
                   190 + i * wheel_spacing + wheel_radius, 400 + wheel_radius), fill='black') 
    draw.ellipse((190 + i * wheel_spacing - (wheel_radius - 10), 400 - (wheel_radius - 10), 
                   190 + i * wheel_spacing + (wheel_radius - 10), 400 + (wheel_radius - 10)), fill='gray') 
 
draw.ellipse((1000 - 20, 300 - 20, 1000 + 20, 300 + 20), fill='yellow') 
 
draw.rectangle((980, 350, 990, 400), fill='black') 
 
 
 
img.show() 
