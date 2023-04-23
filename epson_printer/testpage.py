"""
Creator: Tony DO
Copyright: dvhbkhn@gmail.com
Date: 23.04.23
"""
from epsonprinter import EpsonPrinter
from optparse import OptionParser
import sys, os, time, datetime
from PIL import Image, ImageFont
from PIL import ImageDraw
import textwrap
from time import ctime
import requests


def making_POST_request(url, data):
    url = url
    data = data
    # A POST request to the api
    post_response = requests.post(url, json=data)

    # print the response
    post_response_json = post_response.json()
    print(post_response_json)
    return 0

def gpio_button_ctrl(pin1, pin2):
    if pin1:
        print("I will work after this pin activated")
    if pin2:
        print("I will work after this pin activated")

    return 0


def image_edit(text1, text2, text3,png):
    img = Image.open(png)
    font1 = ImageFont.truetype("../font/arial-unicode-ms.ttf",14)
    font = ImageFont.truetype("../font/arial.ttf",70)
    w_size,h_size  = img.size
    #print(w, " ", h)
    l1 = ImageDraw.Draw(img)
    para = textwrap.wrap(text1, width=50)
    current_h, pad = 120, 10
    for line in para:
        w, h = l1.textsize(line, font=font1)
        l1.text(((w_size - w)/2,current_h), line, font=font1)
        current_h += h + pad
    
    para = textwrap.wrap(text2, width=50)
    current_h, pad = 170, 10
    for line in para:
        w, h = l1.textsize(line, font=font)
        l1.text(((w_size - w)/2,current_h), line, font=font, stroke_width=4)
        current_h += h + pad
    print("see time: ",time.time())

    #l1.text((50,120), text1, fill=0)
    #l1.text((120,180), text2,font=font, fill=0, stroke_width=4 )
    l1.text((138,300), text3, fill = 0)
    angle = 270
    img = img.rotate(angle, expand=True)
    img.show()
    img.save("tmp.png")
    return 0

def text_image(text1, text2, text3,png):
    #img = Image.open(png)
    font1 = ImageFont.truetype("../font/arial-unicode-ms.ttf",14)
    font = ImageFont.truetype("../font/arial.ttf",70)
    #w_size,h_size  = img.size
    #print(w, " ", h)
    w_size, h_size = 350, 400
    img = Image.new('RGB', (w_size, h_size), (255,255,255, 255))
    l1 = ImageDraw.Draw(img)
    para = textwrap.wrap(text1, width=50)
    current_h, pad = 120, 10
    for line in para:
        w, h = l1.textsize(line, font=font1)
        l1.text(((w_size - w)/2,current_h), line, font=font1, fill=(0,0,0,0))
        current_h += h + pad
    
    para = textwrap.wrap(text2, width=50)
    current_h, pad = 170, 10
    for line in para:
        w, h = l1.textsize(line, font=font)
        l1.text(((w_size - w)/2,current_h), line, font=font, stroke_width=4, fill=(0,0,0,0))
        current_h += h + pad
    print("see time: ",time.time())

    #l1.text((50,120), text1, fill=0)
    #l1.text((120,180), text2,font=font, fill=0, stroke_width=4 )
    l1.text((138,300), text3, fill = 0)
    angle = 270
    img = img.rotate(angle, expand=True)
    img.show()
    img.save("tmp.png")
    return 0


if __name__ == '__main__':
    #text1 = "This is address for center it can be long and longer than it is, I think it will be more"
    # text1 = u"Đây là tên dịch vụ cần in theo khách hàng"
    # text2 = "123456"
    # text3 = str(datetime.datetime.now().strftime('%H:%M:%S'))
    # png = "../format_pic.png"
    # test = image_edit(text1, text2, text3, png=png)



    parser = OptionParser()
    parser.add_option("-v", "--idvendor", action="store", type="int",default="0x04b8", dest="id_vendor", help="The printer vendor id")
    parser.add_option("-p", "--idProduct", action="store", type="int",default="0x0e27", dest="id_product", help="The printer product id")
    options, args = parser.parse_args()
    if not options.id_vendor or not options.id_product:
        parser.print_help()
    else:
        printer = EpsonPrinter(options.id_vendor, options.id_product)
        """Text printing"""
        #text1 = "This is address for center it can be long and longer than it is, I think it will be more"
        text1 = u"Đây là tên dịch vụ cần in theo khách hàng"
        text2 = "123456"
        text3 = str(datetime.datetime.now().strftime('%H:%M:%S'))
        png = "../format_pic.png"
        test = text_image(text1, text2, text3, png=png)
        # test = image_edit(text1, text2, text3, png=png)
        # test = image_edit(text1, text2, text3, png=png)
        os.system("sudo lp -o landscape tmp.png")
        time.sleep(13)
        printer.print_text("    =====>>> Have a nice day!    <<<=====\n\n\n")
        printer.linefeed()
        printer.cut()
        sys.exit(1)
