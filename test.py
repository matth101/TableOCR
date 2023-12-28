import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Fullscreen

        self.image_label = tk.Label(self.root)
        self.image_label.pack(expand="yes", fill="both")

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.BOTTOM)

        self.convert_button = tk.Button(self.root, text="Convert and Save", command=self.convert_and_save)
        self.convert_button.pack(side=tk.BOTTOM)

        self.image_path = None
        self.current_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            self.image_path = file_path
            self.display_image()

    def display_image(self):
        image = Image.open(self.image_path)
        image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.current_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_image)

    def convert_and_save(self):
        if self.current_image:
            image = Image.open(self.image_path)
            numpy_array = np.array(image)
            print(numpy_array)
            # Save the numpy array to a file if needed

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
