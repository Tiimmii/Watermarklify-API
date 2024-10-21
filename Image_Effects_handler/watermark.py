from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def apply_watermark(
    image_path,
    output_path,
    text,
    font_path="CaesarDressing-Regular.ttf",
    font_size=36,
    font_bold=False,
    font_italic=False,
    font_underline=False,
    text_color=(255, 255, 255),
    text_opacity=128,
    rotate_angle=0,
    text_position=(0, 0),  # (x, y) position for the watermark
    subscript=False,
    superscript=False,
    line_height=10,
    text_rotation=0
):
    image = Image.open(image_path).convert("RGBA")

    # Create a transparent layer for the watermark text
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(txt_layer)

    # Load the custom font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font {font_path} not found, using default font.")
        font = ImageFont.load_default()

    # Apply text transformation effects (bold/italic are mostly handled with different font files)
    if font_bold:
        font = ImageFont.truetype(font_path, font_size)  # You may need a bold version of your font

    if font_italic:
        font = ImageFont.truetype(font_path, font_size)  # You may need an italic version of your font

    # Apply opacity to text color
    text_color = (*text_color[:3], text_opacity)

    # Add text at the specified position
    draw.text(text_position, text, font=font, fill=text_color)

    # Rotate the text layer (optional)
    if text_rotation != 0:
        txt_layer = txt_layer.rotate(text_rotation, expand=1)

    # Ensure the text layer is the same size as the image and has an alpha channel
    txt_layer = txt_layer.resize(image.size, resample=Image.BILINEAR)

    # Merge the text layer with the original image
    watermarked_image = Image.alpha_composite(image, txt_layer)

    # Save the watermarked image
    watermarked_image.save(output_path, "PNG")


# Usage example with custom position
apply_watermark(
    image_path="ghost.jpg",
    output_path="watermarked_image.png",
    text="Sample Watermark",
    font_path="CaesarDressing-Regular.ttf",
    font_size=200,
    font_bold=True,
    text_color=(0, 255, 0),  # Green color
    text_opacity=128,
    text_rotation=0,  # 15 degrees rotation
    text_position=(400, 100)  # Exact position (x=100, y=200)
)
