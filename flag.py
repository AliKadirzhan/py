from PIL import Image, ImageDraw 

import math 

 

# Define the dimensions of the flag 

width = 760 

height = 400 

stripe_height = height / 13 

union_width = width * 2 / 5 

union_height = stripe_height * 7 

 

# Define darker colors 

dark_red = (64, 64, 64) 

dark_blue = (52, 52, 52) 

white = (255, 255, 255) 

 

# Create a new image with a white background 

img = Image.new("RGB", (width, height), white) 

draw = ImageDraw.Draw(img) 

 

# Draw the stripes 

for i in range(13): 

    stripe_color = dark_red if i % 2 == 0 else white 

    draw.rectangle([0, i * stripe_height, width, (i + 1) * stripe_height], fill=stripe_color) 

 

# Draw the union (blue field) 

draw.rectangle([0, 0, union_width, union_height], fill=dark_blue) 

 

# Function to draw a 5-pointed star 

def draw_star(center_x, center_y, radius, color): 

    points = [] 

    for i in range(5): 

        outer_angle = i * (2 * math.pi / 5) - math.pi / 2 

        inner_angle = outer_angle + math.pi / 5 

 

        outer_x = center_x + radius * math.cos(outer_angle) 

        outer_y = center_y + radius * math.sin(outer_angle) 

 

        inner_x = center_x + (radius / 2) * math.cos(inner_angle) 

        inner_y = center_y + (radius / 2) * math.sin(inner_angle) 

 

        points.append((outer_x, outer_y)) 

        points.append((inner_x, inner_y)) 

 

    draw.polygon(points, fill=color) 

 

# Star layout settings 

star_radius = 13 

rows_of_5_stars = [0, 2, 4]  # Rows with 5 stars 

rows_of_4_stars = [1, 3]     # Rows with 4 stars 

 

# Calculate spacing 

horizontal_spacing_5 = union_width / 5  # Spacing for 5-star rows 

horizontal_spacing_4 = union_width * 0.8 / 4  # Slightly smaller width for 4-star rows 

horizontal_offset_4 = (union_width - (4 * horizontal_spacing_4)) / 2  # Center 4-star rows 

vertical_spacing = union_height / 5  # Spacing between rows 

 

# Loop to draw the stars 

for row in range(5): 

    y_position = row * vertical_spacing + vertical_spacing / 2 

 

    if row in rows_of_5_stars: 

        # Draw 5 stars in this row 

        for col in range(5): 

            x_position = col * horizontal_spacing_5 + horizontal_spacing_5 / 2 

            draw_star(x_position, y_position, star_radius, white) 

    else: 

        # Draw 4 stars in this row, centered 

        for col in range(4): 

            x_position = col * horizontal_spacing_4 + horizontal_offset_4 + horizontal_spacing_4 / 2 

            draw_star(x_position, y_position, star_radius, white) 

 

# Show the image 

img.show() 
