"""
Creator: Tony DO
Copyright: dvhbkhn@gmail.com
Date: 23.04.23
"""
#from epsonprinter import EpsonPrinter
#from optparse import OptionParser
import sys, os, time, datetime
from PIL import Image, ImageFont
from PIL import ImageDraw
import textwrap
from time import ctime
import requests
import RPi.GPIO as GPIO
#import usb.core
import _thread, argparse

# Phần cài đặt kết nối ngoại vi
GPIO.setmode(GPIO.BOARD)
# kết thúc phần cài đặt kết nối ngoại vi
# Hàm input ID và Vendor của máy in
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id_vendor', action='store', dest='id_vendor',
                        help='Store ID of vendor check by: $lsusb')
    parser.add_argument('-id_product', action='store', dest='id_product',
                        help='Store ID product check by: $lsusb')
    parser_value = parser.parse_args()
    id_vendor = parser_value.id_vendor
    id_product = parser_value.id_product
   
    return id_vendor, id_product

"""
 Hàm đẩy dữ liệu JSON lên web service
    input:
        - url = địa chỉ url API
        - data = thông tin data  
"""
def making_POST_request(url, data):
    url = url
    data = data
    # A POST request to the api
    post_response = requests.post(url, json=data)

    # print the response
    post_response_json = post_response.json()
    print("reply from post response: ", post_response_json)
    print("post response status: ", post_response.status_code)
    return 0

"""
    Hàm điều kiểm tra thiết bị ngoại vi 
    input:
        - pin1 = địa chỉ chân GPIO 1
        - pin2 = đại chỉ chân GPIO 2
    output:
        - trạng thái của chân PIN1, PIN2 tương ứng
"""
def gpio_button_ctrl(pin1, pin2):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)
    # print("I'm working with GPIO signal, please following\n")
    # print("status pin ",pin1, " ",  GPIO.input(pin1))
    # print("status pin ", pin2, " ", GPIO.input(pin2))
    return int(GPIO.input(pin1)), int(GPIO.input(pin2))

"""
    Hàm tạo ảnh thông tin 
    input:
        - logo = địa chỉ file logo
        - text1 = kí tực dòng 1
        - text2 = kí tự dòng 2
        - text3 = kí tự dòng 3 thời gian thực 
    output:
        - ảnh output định dạng *png 
"""
def text_image(logo, text1, text2, text3):
    logo = Image.open(logo)
    img_logo = logo.resize((350,86))
    font1 = ImageFont.truetype("./font/arial-unicode-ms.ttf",17) # input your absolute path => for auto running when boot up
    font2 = ImageFont.truetype("./font/arial.ttf",70) # input your absolute path => for auto running when boot up
    font3 = ImageFont.truetype("./font/arial.ttf",15) # input your absolute path => for auto running when boot up
    w_size, h_size = 350, 400
    img = Image.new('RGB', (w_size, h_size), (255,255,255,255))
    img.paste(img_logo,(0,0))

    l1 = ImageDraw.Draw(img)
    para = textwrap.wrap(str(text1), width=50)
    current_h, pad = 120, 10
    for line in para:
        w, h = l1.textsize(line, font=font1)
        l1.text(((w_size - w)/2,current_h), line, font=font1, fill=(0,0,0,0))
        current_h += h + pad
    
    para = textwrap.wrap(str(text2), width=50)
    current_h, pad = 170, 10
    for line in para:
        w, h = l1.textsize(line, font=font2)
        l1.text(((w_size - w)/2,current_h), line, font=font2, stroke_width=1, fill=(0,0,0,0))
        current_h += h + pad
    #print("see time: ",time.time())
    #l1.text((50,120), text1, fill=0)
    #l1.text((120,180), text2,font=font, fill=0, stroke_width=4 )
    l1.text((138,300), str(text3), fill = 0,font=font3)
    angle = 270
    img = img.rotate(angle, expand=True)
    img.show()
    img.save("tmp.png") # input your absolute path => for auto running when boot up
    return 0

if __name__ == '__main__':
    id_vendor, id_product = parser()
    
    #GPIO nhập địa chỉ chân PIN GPIO
    pin1 = 13
    pin2 = 15
    text2 = 100 # giá trị khởi tạo counter
    while True:
        # Kiểm tra trạng thái nút bấm
        pin1_status, pin2_status = gpio_button_ctrl(pin1, pin2)

        while(pin1_status==1 or pin2_status==1):
            pin1_status = 0
            pin2_status = 0
            print("You pressed the button\n")
            """Text printing"""
            logo_img = "../logo.bmp" # đường dẫn logo image
            text1 = u"Phần in tên dịch vụ cần in theo khách hàng" # tên text 
            text2 = text2 + 1 # số thứ tự
            text3 = str(datetime.datetime.now().strftime('%H:%M:%S'))
            test = text_image(logo_img, text1, str(text2), text3)
            #cmd = "sudo lp -o landscape tmp.png && sudo python cut.py -id_vendor " + str(id_vendor) + " -id_product " + str(id_product)
            #os.system(str(cmd))
            os.system("sudo lp -o landscape tmp.png && sudo python cut.py ") # chạy chương trình in máy EPSON
            time.sleep(2) # thời gian delay = 2seconds
            # Threading cho việc pust data lên web service
            #url = "https://jsonplaceholder.typicode.com/posts/"
            url = "https://datcom.click/api.lay-so-thu-tu"
            data = {"id_donvi":"1", "id_dichvu":"1", "phone": "095551234", "name":"Trần Đình Hợp"}
            #data = {"text1": text1, "text2": text2, "text3": text3}
            thread1 = _thread.start_new_thread(making_POST_request, (url, data))
            # kết thúc chạy thread cho đẩy dữ liệu lên web service
            pin1_status = 0
            pin2_status =0
            os.remove("tmp.png") # input your absolute path
            # hoàn thành việc in và chờ người dùng ấn nút tiếp theo
    sys.exit(1)
