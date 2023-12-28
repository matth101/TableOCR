import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_button = ttk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.convert_button = ttk.Button(root, text="Convert and Save", command=self.convert_and_save)
        self.convert_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.image_path = None
        self.current_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            self.image_path = file_path
            self.display_image()

    def display_image(self):
        if self.current_image:
            self.current_image.destroy()

        image = Image.open(self.image_path)
        image.thumbnail((800, 600))  # Adjust the dimensions as needed
        self.current_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(self.frame, width=image.width, height=image.height)
        canvas.pack(expand="yes", fill="both")
        canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)

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
