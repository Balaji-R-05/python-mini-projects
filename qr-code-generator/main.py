import qrcode as qr # Library to generate QR codes

# data = "https://www.github.com/Balaji-R-05"
# qr_code = qr.make(data)
# qr_code.save("qrcode.png")

qr_code = qr.QRCode(
    version=1,  # Size of the QR code (1 is the smallest, up to 40)
    error_correction=qr.ERROR_CORRECT_H,  # Sets the error correction level to High (~30% can be recovered)
    box_size=10,  # Size of each box (module) in pixels
    border=6  # Width of the white border around the QR code (minimum is 4)
)

data = input("Enter the data to be encoded in the QR code: ")
qr_code.add_data(data)
qr_code.make(fit=True)

img = qr_code.make_image(
    fill_color="Red",  # Color of the QR code H
    back_color="White"  # Background color of the QR code
)
img.save("qr-code-generator\demo.png")