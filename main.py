from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageFont, ImageTk, UnidentifiedImageError

WIDTH, HEIGHT = 1280,720
CANVAS_WIDTH, CANVAS_HEIGHT = 1270, 685

def upload_image():
    try:
        img_path = askopenfilename()
        im = Image.open(img_path)
        img_width, img_height = im.size

        if img_width > CANVAS_WIDTH or img_height > CANVAS_HEIGHT:
            while img_width > CANVAS_WIDTH or img_height > CANVAS_HEIGHT:
                img_width *= .99
                img_height *= .99

            im = im.resize((int(img_width), int(img_height)))

        watermark_text = marca_entry.get()

        if len(watermark_text) == 0 :
            messagebox.showinfo(title="Erro", message="Preencha  o campo de marca d'agua")

        draw = ImageDraw.Draw(im)
        font_size = 18
        font = ImageFont.truetype("arial.ttf", font_size)
        text_color = (0, 00, 0)

        # White color (RGB)
        bbox = draw.textbbox((0, 0), watermark_text, font)
        # bbox format - (left, top, right, bottom)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        image_width, image_height = im.size
        margin = 10

        # Margin from the right and bottom edges
        position = (image_width - text_width - margin, image_height - text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)
        im.save("image/watermarked_image.png")

        img =  ImageTk.PhotoImage(im)
        canvas.img = img
        canvas.itemconfig(imagem, image=img)
    except UnidentifiedImageError:
        messagebox.showinfo("Erro Upload!",
                            "Imagem não enviada. Por favor selecione uma mensagem.")

window = Tk()
window.title("marca d'água sua imagem")
window.geometry('%sx%s' % (WIDTH,HEIGHT))

canvas = Canvas(window,width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
imagem = canvas.create_image(600, 300,anchor=CENTER)
canvas.grid(row=1, column=0, columnspan=15)

botao_upload = Button(window,text="Selecionar Imagem",width=15, command=upload_image)
botao_upload.grid(row=0, column=0)

marca_label = Label(text="Marca d'agua:",width=10)
marca_label.grid(row=0,column=1)
marca_entry = Entry(width=25)
marca_entry.grid(row=0,column=2)
marca_entry.focus()

window.mainloop()