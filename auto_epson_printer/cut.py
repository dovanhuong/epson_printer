import os, time, argparse
from escpos.printer import Usb
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
if __name__=="__main__":
    id_vendor, id_product = parser()
    #p = Usb(str(id_vendor), str(id_product),0)
    p = Usb(0x04b8, 0x0e27,0)  # input your value of id_vendor and id_product by $lsusb
    p.cut()
