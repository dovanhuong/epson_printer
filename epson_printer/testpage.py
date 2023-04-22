"""
Creator: Tony DO
Copyright: dvhbkhn@gmail.com
Date: 23.04.23
"""
from epsonprinter import EpsonPrinter
from optparse import OptionParser
import sys, os, time
from PIL import Image, ImageFont
from PIL import ImageDraw


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
    font = ImageFont.truetype("./font/arial.ttf",70)
    w,h  = img.size
    print(w, " ", h)

    l1 = ImageDraw.Draw(img)
    l1.text((50,120), text1, fill=0)
    l1.text((140,200), text2,font=font, fill=0 )
    l1.text((180,300), text3, fill = 0)
    #img.show()
    img.save("tmp.png")
    return 0

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-v", "--idvendor", action="store", type="int",default="0x04b8", dest="id_vendor", help="The printer vendor id")
    parser.add_option("-p", "--idProduct", action="store", type="int",default="0x0e27", dest="id_product", help="The printer product id")
    options, args = parser.parse_args()
    if not options.id_vendor or not options.id_product:
        parser.print_help()
    else:
        printer = EpsonPrinter(options.id_vendor, options.id_product)
        """Text printing"""
        text1 = "This is address for center"
        text2 = "10000"
        text3 = "24:24:30"
        png = "1.png"
        test = image_edit(text1, text2, text3, png=png)
        os.system("sudo lp -o landscape tmp.png")
        time.sleep(13)
        printer.print_text("    =====>>> Have a nice day!    <<<=====\n\n\n")
        printer.linefeed()
        printer.cut()
        sys.exit(1)
