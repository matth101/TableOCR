import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageCropperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper App")

        self.image_path = None
        self.original_image = None
        self.cropped_image = None

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_click_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_release)

        self.crop_start = None
        self.crop_rect_id = None

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Crop Image", command=self.crop_image)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(self.image_path)
            self.display_image()

    def display_image(self):
        if self.original_image:
            tk_image = ImageTk.PhotoImage(self.original_image)
            self.canvas.config(width=tk_image.width(), height=tk_image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            self.canvas.tk_image = tk_image

    def on_click_press(self, event):
        self.crop_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
        x, y = self.crop_start
        x1, y1 = event.x, event.y
        self.crop_rect_id = self.canvas.create_rectangle(x, y, x1, y1, outline="red")

    def on_click_release(self, event):
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
        x, y = self.crop_start
        x1, y1 = event.x, event.y
        self.cropped_image = self.crop_image_region(x, y, x1, y1)
        # You can now use self.cropped_image as a NumPy array or for further processing
        self.display_cropped_image()

    def crop_image_region(self, x, y, x1, y1):
        if self.original_image:
            region = self.original_image.crop((x, y, x1, y1))
            return np.array(region)

    def display_cropped_image(self):
        if self.cropped_image is not None:
            cropped_tk_image = ImageTk.PhotoImage(Image.fromarray(self.cropped_image))
            self.canvas.config(width=cropped_tk_image.width(), height=cropped_tk_image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=cropped_tk_image)
            self.canvas.tk_image = cropped_tk_image

    def crop_image(self):
        if self.image_path:
            crop_window = tk.Toplevel(self.master)
            crop_app = ImageCropperApp(crop_window)
            crop_app.image_path = self.image_path
            crop_app.original_image = self.original_image
            crop_app.display_image()

def main():
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
