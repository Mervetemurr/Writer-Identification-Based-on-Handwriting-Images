from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from tensorflow import keras
import numpy as np

class Window:
    def __init__(self, win, ww, wh):
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 350, 200))
        self.win.title("El yazısından yazar tespiti")
        self.path = None
        self.color = ["#4f4e4d", "#f29844", "red2"]

        self.can1 = Canvas(self.win, width=605, height=355, bg='white', relief='solid', borderwidth=1)
        self.can1.place(x=35, y=5)

        self.button1 = Button(self.win, text='Dosya seç', width=10, height=1, command=self.load_show_img)
        self.button1.place(x=180, y=380)
        self.button2 = Button(self.win, text='Yazarı bul', width=10, height=1, command=self.predict)
        self.button2.place(x=280, y=380)
        self.button3 = Button(self.win, text='Temizle', width=10, height=1, command=self.clear)
        self.button3.place(x=380, y=380)
        self.model_c = keras.models.load_model("keras_model.h5")


    def load_show_img(self):
        sv = StringVar()
        sv.set(askopenfilename())
        self.path = Entry(self.win, state='readonly', text=sv).get()  # 获取到了所打开的图片
        img_open = Image.open(self.path).resize((600, 350))
        self.img_Tk = ImageTk.PhotoImage(img_open)
        self.can1.create_image(6, 6, image=self.img_Tk, anchor='nw')

    def predict(self):
        from PIL import Image, ImageOps
        from tensorflow import keras
        np.set_printoptions(suppress=True)  # Disable scientific notation for clarity
        model = keras.models.load_model('keras_model.h5')  # Load the model
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(self.path)  # Replace this with the path to your image
        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        image_array = np.asarray(image)  # turn the image into a numpy array
        # image.show() # display the resized image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1  # Normalize the image
        data[0] = normalized_image_array  # Load the image into the array
        class_names = ["fatih", "muhammed", "levent"]

        prediction = model.predict(data)  # run the inference
        pre=class_names[np.argmax(prediction[0])]
        self.label2 = Label(self.win, text="El yazısının sahibi:", font="12")
        self.label2.place(x=180, y=415)
        self.can3 = Canvas(self.win, width=140, height=25, bg='white', relief='solid', borderwidth=1)
        self.can3.place(x=320, y=412)
        self.can3.create_text(50,15,text=pre, font="Times 15")

    def clear(self):
        self.can1.delete("all")
        #self.can2.delete("all")
        self.can3.delete("all")
        self.path = None

    def closeEvent():
        keras.backend.clear_session()
        sys.exit()


if __name__ == '__main__':
    win = Tk()
    ww = 700
    wh = 480
    Window(win, ww, wh)
    win.protocol("WM_DELETE_WINDOW", Window.closeEvent)
    win.mainloop()