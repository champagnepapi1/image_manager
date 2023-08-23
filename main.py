from PIL import Image
import math

def convert_image(image_path, output_path):
    input_image = Image.open(image_path)
    input_image = input_image.convert("RGBA")  

    
    if input_image.size != (512, 512):
        new_image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        offset = ((512 - input_image.width) // 2, (512 - input_image.height) // 2)
        new_image.paste(input_image, offset)
        input_image = new_image

    pixels = input_image.load()

   
    output_image = Image.new("RGBA", input_image.size)
    draw = ImageDraw.Draw(output_image)

   
    for i in range(512):
        for j in range(512):
            r, g, b, a = pixels[i, j]
            distance_to_center = math.sqrt((i-256)**2 + (j-256)**2)
            if distance_to_center <= 256 and (is_close_to_yellow((r, g, b)) or is_black((r, g, b))):
                draw.point((i, j), fill=(r, g, b, a))
            elif distance_to_center > 256 and (is_black((r, g, b)) or is_close_to_yellow((r, g, b))):
                draw.point((i, j), fill=(r, g, b, a))
            else:
                draw.point((i, j), fill=(0, 0, 0, 0))  

    output_image.save(output_path, format="PNG")


def is_close_to_yellow(color):
    r, g, b = color
    if r > 200 and g > 200 and b < 100:
        return True
    return False

def verify_image(image_path):
    image = Image.open(image_path)
    if image.format != 'PNG':
        return False
    if image.size != (512, 512):
        return False

    pixels = image.load()
    yellow_count = 0
    total_inside_circle = 0

    for i in range(512):
        for j in range(512):
            distance_to_center = math.sqrt((i-256)**2 + (j-256)**2)
            if distance_to_center <= 256:
                total_inside_circle += 1
                if is_close_to_yellow(pixels[i, j][:3]):
                    yellow_count += 1
            else:
                
                if pixels[i, j][3] != 0:
                    return False

    if yellow_count / total_inside_circle >= 0.5:
        return True
    else:
        return False

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    result = verify_image(image_path)
    if result:
        print("The image meets the requirements.")
    else:
        print("The image does not meet the requirements.")
