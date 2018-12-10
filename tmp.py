from PIL import Image, ImageDraw, ImageFont
import os

def center_anchor(x, y, text, font, draw):
    w, h = draw.textsize(text, font=font)
    new_x = x - w / 2
    new_y = y - h / 2
    return [new_x, new_y]

font = ImageFont.truetype('Arial.ttf', 20)
screenshot = Image.new('RGB', (900, 556), (255, 255, 255))
draw = ImageDraw.Draw(screenshot)
draw.text(center_anchor(450, 530, 'Time (Seconds)', font, draw), 'Time (Seconds)', (0,0,0), font, anchor='center')
draw.line([0, 0, 900, 556], (0,0,0))
draw.line([450, 556, 450, 0], (0,0,0))

prefix = [0]
for name in os.listdir('screenshots'):
    print(name)
    prefix.append(int(name[6:-4]))

screenshot.save('screenshots/figure'+str(max(prefix)+1)+'.jpg')
