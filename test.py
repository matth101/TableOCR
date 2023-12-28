import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")  # Set your desired initial dimensions

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand="yes", fill="both")

        self.load_button = ttk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.convert_button = ttk.Button(self.root, text="Convert and Save", command=self.convert_and_save)
        self.convert_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.image_path = None
        self.current_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            self.image_path = file_path
            self.display_image()

    def display_image(self):
        image = Image.open(self.image_path)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()))
        self.current_image = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)

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
