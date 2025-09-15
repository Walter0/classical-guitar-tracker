#!/usr/bin/env python3
"""
Create a PNG icon for the Classical Guitar Learning Tracker
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_guitar_icon():
    """Create a 512x512 PNG icon for the app"""
    
    # Create a 512x512 image with transparent background
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors (earth tones matching the app)
    bg_color = (245, 242, 232, 255)      # #f5f2e8
    primary_color = (139, 115, 85, 255)   # #8b7355
    secondary_color = (160, 149, 107, 255) # #a0956b
    accent_color = (212, 196, 160, 255)   # #d4c4a0
    dark_color = (74, 64, 53, 255)       # #4a4035
    
    # Create background circle
    margin = 20
    circle_size = size - (margin * 2)
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=bg_color, outline=primary_color, width=8)
    
    # Guitar body (simplified)
    body_center = (size//2, size//2 + 30)
    body_width = 90
    body_height = 120
    body_rect = [
        body_center[0] - body_width//2,
        body_center[1] - body_height//2,
        body_center[0] + body_width//2,
        body_center[1] + body_height//2
    ]
    draw.ellipse(body_rect, fill=accent_color, outline=primary_color, width=4)
    
    # Sound hole
    hole_size = 30
    hole_rect = [
        body_center[0] - hole_size//2,
        body_center[1] - hole_size//2,
        body_center[0] + hole_size//2,
        body_center[1] + hole_size//2
    ]
    draw.ellipse(hole_rect, fill=dark_color)
    
    # Guitar neck
    neck_width = 12
    neck_top = 80
    neck_bottom = body_center[1] - body_height//2
    neck_rect = [
        size//2 - neck_width//2,
        neck_top,
        size//2 + neck_width//2,
        neck_bottom
    ]
    draw.rectangle(neck_rect, fill=primary_color)
    
    # Guitar strings (simplified)
    string_positions = [-15, -9, -3, 3, 9, 15]
    for pos in string_positions:
        x = size//2 + pos
        draw.line([(x, neck_top), (x, size - 60)], fill=dark_color, width=2)
    
    # Guitar head
    head_rect = [
        size//2 - 26,
        neck_top - 30,
        size//2 + 26,
        neck_top
    ]
    draw.rectangle(head_rect, fill=secondary_color, outline=primary_color, width=2)
    
    # Tuning pegs
    peg_positions = [-15, 0, 15]
    for pos in peg_positions:
        peg_center = (size//2 + pos, neck_top - 15)
        draw.ellipse([peg_center[0]-4, peg_center[1]-4, 
                     peg_center[0]+4, peg_center[1]+4], fill=primary_color)
    
    # Add musical note
    note_size = 60
    note_x = size//2 + 80
    note_y = 120
    
    try:
        # Try to use a system font for the musical note
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", note_size)
        draw.text((note_x, note_y), "♪", fill=primary_color, font=font, anchor="mm")
    except:
        # Fallback to default font
        draw.text((note_x, note_y), "♪", fill=primary_color, anchor="mm")
    
    return img

def main():
    """Create the icon files"""
    print("🎨 Creating Classical Guitar Learning Tracker icon...")
    
    # Create the main icon
    icon = create_guitar_icon()
    
    # Save as PNG
    png_path = "guitar_icon.png"
    icon.save(png_path, "PNG")
    print(f"✅ Created {png_path}")
    
    # Create different sizes for better icon quality
    sizes = [16, 32, 64, 128, 256, 512]
    icon_dir = "icon_files"
    
    if not os.path.exists(icon_dir):
        os.makedirs(icon_dir)
    
    for size in sizes:
        resized = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f"{icon_dir}/icon_{size}x{size}.png", "PNG")
    
    print(f"✅ Created multiple icon sizes in {icon_dir}/")
    print("🎸 Icon creation complete!")

if __name__ == "__main__":
    main()