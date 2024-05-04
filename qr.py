import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas as pd
import tempfile
import os

def generate_qr_on_flyer(data, pdf_filename, flyer_path):
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    cols, rows = 3, 4  # По умолчанию
    x_step = width / cols
    y_step = height / rows

    for idx, row in enumerate(data.itertuples()):
        offer_url = f"https://offer.store/offers/{row.Offer}"
        qrcode_img = qrcode.make(offer_url)
        qr_temp_file_path = tempfile.mktemp(suffix='.png')
        qrcode_img.save(qr_temp_file_path)

        flyer_image = Image.open(flyer_path)
        qr_image = Image.open(qr_temp_file_path)
        qr_size = (int(flyer_image.width / 4), int(flyer_image.height / 4))
        qr_image = qr_image.resize(qr_size, Image.Resampling.LANCZOS)

        position = (flyer_image.width - qr_size[0] - 10, flyer_image.height - qr_size[1] - 10)
        flyer_image.paste(qr_image, position, qr_image)

        combined_temp_file_path = tempfile.mktemp(suffix='.png')
        flyer_image.save(combined_temp_file_path)

        x_pos = (idx % cols) * x_step + 10
        y_pos = height - ((idx // cols) + 1) * y_step + 10

        # Рисуем комбинированное изображение на странице
        c.drawImage(combined_temp_file_path, x_pos, y_pos, x_step - 20, y_step - 20)

        os.remove(qr_temp_file_path)
        os.remove(combined_temp_file_path)

        # Добавляем номер партии
        if (idx + 1) % (cols * rows) == 0 or idx + 1 == len(data):
            # batch_number = f"1{row.Offer}"
            c.drawString(5, height - 10, "1A")  # В верхнем левом углу
            c.showPage()

    c.save()

def main():
    offers = pd.DataFrame({
        'Offer': ['5', '4', '7', '9', '2', '119', '550', '514', '515', '3', '325', '302']
    })
    generate_qr_on_flyer(offers, 'qr_codes_on_flyers.pdf', 'D:\projects\qr_codes\IMG-20230427-WA0007.jpg')

if __name__ == '__main__':
    main()
