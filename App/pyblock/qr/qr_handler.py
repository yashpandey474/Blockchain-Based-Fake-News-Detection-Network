import segno
from PIL import Image

def make_qr(text:str):
    qr = segno.make_qr(text)
    qr.save("qr.png",scale = 20)
    Image.open("qr.png").show()
    return "qr.png"

if __name__ == "__main__":
    make_qr("Hello World")