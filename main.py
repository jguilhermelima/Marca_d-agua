from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageFont, ImageTk, UnidentifiedImageError

WIDTH, HEIGHT = 1280,720
CANVAS_WIDTH, CANVAS_HEIGHT = 1277, 690

def upload_image():
    try:
        img_path = askopenfilename()
        imagem_original = Image.open(img_path)
        img_width, img_height = imagem_original.size

        if img_width > CANVAS_WIDTH or img_height > CANVAS_HEIGHT:
            while img_width > CANVAS_WIDTH or img_height > CANVAS_HEIGHT:
                img_width *= .99
                img_height *= .99

            imagem_original = imagem_original.resize((int(img_width), int(img_height)))

        imagem_tk = ImageTk.PhotoImage(imagem_original)
        canvas.img = imagem_tk
        canvas.itemconfig(imagem_canvas, image=imagem_tk)
        imagem_original.save("imagem/imagem_marca_dagua.png")

    except UnidentifiedImageError:
        messagebox.showinfo("Erro Upload!",
                            "Imagem não enviada. Por favor selecione uma Imagem.")

def inserir_marca():
    img_selecionada = Image.open("imagem/imagem_marca_dagua.png").convert("RGBA")
    txt = Image.new("RGBA", img_selecionada.size, (255, 255, 255, 0))
    watermark_text = marca_entry.get()

    if len(watermark_text) == 0:
        messagebox.showinfo(title="Erro", message="Preencha  o campo de marca d'agua")

    draw = ImageDraw.Draw(txt)
    font_size = 18
    font = ImageFont.truetype("calibri.ttf", font_size)
    text_color = (255, 255, 255, 128)

    bbox = draw.textbbox((0, 0), watermark_text, font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    image_width, image_height = img_selecionada.size
    margin = 10

    local_marca = localizacao_marca()
    if local_marca == "centro":
        position = ((image_width - text_width) / 2, (image_height - text_height) / 2)
        draw.text(position, watermark_text, font=font, fill=text_color)
    elif local_marca == "esquerda superior":
        position = (text_width - margin, text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)
    elif local_marca == "direita superior":
        position = (image_width - text_width - margin, text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)
    elif local_marca == "esquerda inferior":
        position = (text_width - margin, image_height - text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)
    elif local_marca == "direita inferior":
        position = (image_width - text_width - margin, image_height - text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)

    img_marcada = Image.alpha_composite(img_selecionada, txt)

    img_salvar = ImageTk.PhotoImage(img_marcada)
    canvas.img = img_salvar
    canvas.itemconfig(imagem_canvas, image=img_salvar)

    img_marcada.save("imagem/imagem_marca_dagua.png")


def localizacao_marca():
    local =  marca_combobox.get()
    return local

window = Tk()
window.title("Criador de Marca d'Água")
window.config(bg="#FCF4DC")
window.geometry('%sx%s' % (WIDTH,HEIGHT))

canvas = Canvas(window,width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
imagem_canvas = canvas.create_image(635, 325)
canvas.grid(row=1, column=0, columnspan=15)

botao_upload = Button(window,text="Selecionar Imagem",width=16, command=upload_image, bg="#FCF4DC", font=("cascadia", 8, "bold"))
botao_upload.grid(row=0, column=0)

combobox_label = Label(text="Selecione local marca d'agua:", width=22, bg="#FCF4DC", font=("cascadia", 8, "bold"))
combobox_label.grid(row=0, column=1)
combobox_label.grid(row=0,column=1, sticky=E)

marca_combobox = ttk.Combobox(window, values=["centro", "esquerda superior", "direita superior", "esquerda inferior", "direita inferior"],  font=("cascadia", 8, "bold"))
marca_combobox.set("centro")
marca_combobox.grid(row=0,column=2, sticky=W)

marca_label = Label(text="Marca d'agua:",width=10, bg="#FCF4DC", font=("cascadia", 8, "bold"))
marca_label.grid(row=0,column=3, sticky=E)
marca_entry = Entry(width=20)
marca_entry.grid(row=0,column=4, sticky=W)

botao_marcar = Button(window,text="Inserir Marca",width=15, command=inserir_marca, bg="#FCF4DC", font=("cascadia", 8, "bold"))
botao_marcar.grid(row=0, column=5)

window.mainloop()