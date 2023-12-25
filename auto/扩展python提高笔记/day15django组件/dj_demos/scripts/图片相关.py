"""
pip3 install pillow
"""

from PIL import Image, ImageDraw,ImageFont

img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))

draw = ImageDraw.Draw(img, mode='RGB')

font = ImageFont.truetype("Monaco.ttf", 28)

draw.text([0, 0], 'python', "red", font=font)

# 保存在本地
with open('code.png', 'wb') as f:
    img.save(f, format='png')
