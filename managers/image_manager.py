from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageOps


class ImageManager:
    
    LIGHT_SEARCH_IMAGE = Image.open("images/light_search_icon.png")
    DARK_SEARCH_IMAGE = Image.open("images/dark_search_icon.png")

    def circle_mask(image: Image.Image) -> Image.Image:
                

        width, height = image.size

        circle_mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        draw = ImageDraw.Draw(circle_mask)
        draw.ellipse((0, 0, width, height), fill=(255, 255, 255, 255))

        output = ImageOps.fit(image, (width, height), centering=(0.5, 0.5))
        output.putalpha(circle_mask.getchannel("A"))
                 
        return output
    
    def web_image(url: str) -> Image.Image:
        response = requests.get(url)
        bytes_image = BytesIO(response.content)
        image = Image.open(bytes_image)
        return image
