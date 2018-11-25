from segno import helpers
import segno
from PIL import Image
import PIL
import os


def create_QRcode(QRtype, parameters):

    if QRtype == "url":
        qr = segno.make(parameters['url'], micro=False)

    if QRtype == "vcard":
        qr = helpers.make_vcard(name=parameters['vcard']['lastname']+";"+parameters['vcard']['firstname'],
                                displayname=parameters['vcard']['displayname'],
                                email=parameters['vcard']['email'],
                                url=parameters['vcard']['url']
                                )
    if QRtype == "wifi":
        qr = helpers.make_wifi(ssid=parameters["wifi"]['ssn'],
                               password=parameters["wifi"]['password'],
                               security=parameters["wifi"]['security']
                               )
    return qr


def combine_images(picture, qr_code, alpha=0.5):

    # Open pictures:
    picture = Image.open(picture)
    qr_code = Image.open(qr_code)

    # Resize picture to qr_code size:
    basewidth = qr_code.size[1]
    wpercent = (basewidth / float(picture.size[0]))
    hsize = int(float(picture.size[1]) * float(wpercent))
    #picture = picture.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    picture = picture.resize(qr_code.size)
    #print("QR-Coce Size: ", qr_code.size)
    #print("picture Size: ", picture.size)
#### TO-DO #############################################################
# convert image to same datatype (e.g. png)
########################################################################
    qr_code = qr_code.convert("RGBA")
    qr_picture = Image.blend(picture, qr_code, alpha)

    return qr_picture


if __name__ == "__main__":

    dirname = os.path.dirname(__file__) + "/images/"

    # User Inputs:
    picture = "IMG_0416.png"
    picture = 'IMG_2774.png'
    picture = 'starbucks.png'
    picture = 'IMG_4335.png'
    picture = "wifi.png"
    #picture = "IMG_2774.png"
    qr_type = "url"
    parameters={"filetype":"png",
                "border": None,
                "background": None,
                "url": "http://krone.at",
                "wifi":{"ssn": "23452352345",
                        "password": "hallihalo",
                        "security": "WPA"},
                "vcard":{"firstname": "Micky",
                        "lastname": "Mouse",
                        "displayname": "MC",
                        "phone": "+1 23344444",
                        "email": ("micky@me.com", "micky@gmail.com"),
                        "url": ["mickymouse.com", "mickymouse.de"]},     
                }

    #print(type(parameters["vcard"]['email']))
    filetype = parameters['filetype']

    # Create QR
    qr = create_QRcode(qr_type, parameters)
    qr.save(dirname + 'QRcode_final.' + filetype, scale=10, background=None)

    # Create QR-Image
    qr_code = Image.open(dirname + "QRcode_final." + filetype)

    qr_pic = combine_images(dirname + picture,
                    dirname + "QRcode_final." + filetype, alpha=0.5)

    qr_pic.save(dirname + 'qr_picture.' + filetype)
