import segno
from PIL import Image


def make_qr(text:str, show = 0, id=""):
    qr = segno.make_qr(text)
    qr.save(f"Generated_QRs/{id}.png",scale = 20)

    if show:
        Image.open(f"Generated_QRs/{id}.png").show()

    return f"Generated_QRs/{id}.png"

# if __name__ == "__main__":
#     make_qr("Hello World", show = 1)