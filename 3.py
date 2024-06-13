import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps

# Class for image processing
class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
    
    # Method to open an image file
    def open_image(self, filename):
        try:
            self.original_image = Image.open(filename)
            self.processed_image = self.original_image.copy()
            return True
        except:
            messagebox.showerror("Error", "Failed to open image.")
            return False
        
    # Method to apply scaling to the image
    def apply_scaling(self, scale_x, scale_y):
        try:
            self.processed_image = self.original_image.resize((int(scale_x), int(scale_y)), Image.BILINEAR)
            return True
        except:
            messagebox.showerror("Error", "Failed to apply scaling.")
            return False
    
    # Method to apply projection to the image
    def apply_projection(self, points):
        try:
            # Projection of an image fragment onto an arbitrary plane
            self.processed_image = self.original_image.transform(
                (300, 300), Image.QUAD, points, resample=Image.BILINEAR
            )
            return True
        except:
            messagebox.showerror("Error", "Failed to perform projection.")
            return False

    # Method to apply translation to the image    
    def apply_translation(self, translate_x, translate_y):
        try:
            self.processed_image = self.original_image.transform(
                self.original_image.size, Image.AFFINE, (1, 0, translate_x, 0, 1, translate_y)
            )
            return True
        except:
            messagebox.showerror("Error", "Failed to apply translation.")
            return False

    # Method to apply flipping to the image   
    def apply_flip(self, direction):
        try:
            if direction == "horizontal":
                self.processed_image = self.original_image.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == "vertical":
                self.processed_image = self.original_image.transpose(Image.FLIP_TOP_BOTTOM)
            return True
        except:
            messagebox.showerror("Error", "Failed to apply flipping.")
            return False
    
    # Method to apply rotation to the image
    def apply_rotation(self, angle, center):
        try:
            self.processed_image = self.original_image.rotate(angle, resample=Image.BILINEAR, center=center)
            return True
        except:
            messagebox.showerror("Error", "Failed to apply rotation.")
            return False

    def apply_projection(self, points):
        try:
            # Projection of an image fragment onto an arbitrary plane
            self.processed_image = self.original_image.transform(
                (300, 300), Image.QUAD, points, resample=Image.BILINEAR
            )
            return True
        except:
            messagebox.showerror("Error", "Failed to perform projection.")
            return False

# Class for the image processing GUI application
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processor")

        self.image_processor = ImageProcessor()

        self.left_panel = tk.LabelFrame(self, text="Original Image")
        self.left_panel.grid(row=0, column=0, padx=10, pady=10)

        self.right_panel = tk.LabelFrame(self, text="Processed Image")
        self.right_panel.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = tk.Button(self, text="Load Image", command=self.load_images)
        self.load_button.grid(row=1, columnspan=2, pady=10)

        self.scale_x_label = tk.Label(self, text="Scale X:")
        self.scale_x_label.grid(row=2, column=0, padx=5)
        self.scale_x_entry = tk.Entry(self, width=10)
        self.scale_x_entry.grid(row=2, column=1, padx=5)
        self.scale_y_label = tk.Label(self, text="Scale Y:")
        self.scale_y_label.grid(row=3, column=0, padx=5)
        self.scale_y_entry = tk.Entry(self, width=10)
        self.scale_y_entry.grid(row=3, column=1, padx=5)

        self.scale_button = tk.Button(self, text="Scale", command=self.scale_image)
        self.scale_button.grid(row=4, columnspan=2, pady=10)

        self.angle_label = tk.Label(self, text="Rotation Angle (degrees):")
        self.angle_label.grid(row=5, column=0, padx=5)
        self.angle_entry = tk.Entry(self, width=10)
        self.angle_entry.grid(row=5, column=1, padx=5)

        self.rotate_button = tk.Button(self, text="Rotate", command=self.rotate_image)
        self.rotate_button.grid(row=6, columnspan=2, pady=10)

        self.flip_horizontal_button = tk.Button(self, text="Flip Horizontally", command=lambda: self.flip_image("horizontal"))
        self.flip_horizontal_button.grid(row=7, columnspan=2, pady=5)

        self.flip_vertical_button = tk.Button(self, text="Flip Vertically", command=lambda: self.flip_image("vertical"))
        self.flip_vertical_button.grid(row=8, columnspan=2, pady=5)

        self.left_panel.grid_propagate(False)
        self.right_panel.grid_propagate(False)

    # Method to load an image from a file
    def load_images(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success = self.image_processor.open_image(file_path)
            if success:
                self.show_images()

    # Method to apply scaling to the image
    def scale_image(self):
        scale_x = self.scale_x_entry.get()
        scale_y = self.scale_y_entry.get()
        if scale_x and scale_y:
            success = self.image_processor.apply_scaling(float(scale_x), float(scale_y))
            if success:
                self.show_images()

    # Method to apply rotation to the image
    def rotate_image(self):
        angle = self.angle_entry.get()
        if angle:
            angle = float(angle)
            center = (self.image_processor.original_image.width // 2, self.image_processor.original_image.height // 2)
            success = self.image_processor.apply_rotation(angle, center)
            if success:
                self.show_images()

    # Method to apply flipping to the image in the specified direction
    def flip_image(self, direction):
        success = self.image_processor.apply_flip(direction)
        if success:
            self.show_images()

    # Method to update the displayed images in the GUI
    def show_images(self):
        original_image_tk = ImageTk.PhotoImage(self.image_processor.original_image)
        processed_image_tk = ImageTk.PhotoImage(self.image_processor.processed_image)

        self.original_label = tk.Label(self.left_panel, image=original_image_tk)
        self.original_label.image = original_image_tk
        self.original_label.grid(row=0, column=0)

        self.processed_label = tk.Label(self.right_panel, image=processed_image_tk)
        self.processed_label.image = processed_image_tk
        self.processed_label.grid(row=0, column=0)

        self.left_panel.config(width=original_image_tk.width(), height=original_image_tk.height())
        self.right_panel.config(width=processed_image_tk.width(), height=processed_image_tk.height())

    # Method to apply rotation to the original image by a specified angle around the specified center
    def apply_rotation(self, angle, center):
        try:
            self.processed_image = self.original_image.rotate(angle, resample=Image.BILINEAR, center=center)
            return True
        except:
            messagebox.showerror("Error", "Failed to apply rotation.")
            return False

    # Method to perform the projection of an image fragment onto an arbitrary plane defined by four points
    def apply_projection(self, points):
        try:
            width, height = self.original_image.size
            src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
            dst_points = np.float32([tuple(coord) for coord in points])
            matrix = cv2.getPerspectiveTransform(src_points, dst_points)
            processed_image_np = cv2.warpPerspective(np.array(self.original_image), matrix, (width, height))            
            self.processed_image = Image.fromarray(processed_image_np)
            return True
        except Exception as e:
            messagebox.showerror("Error", "Failed to perform projection: " + str(e))
            return False

    # Method rotate_image calls the apply_rotation method to apply rotation to the image with an angle specified by the user through the application interface
    def rotate_image(self):
        angle = self.angle_entry.get()
        if angle:
            angle = float(angle)
            center = (self.image_processor.original_image.width // 2, self.image_processor.original_image.height // 2)
            success = self.image_processor.apply_rotation(angle, center)
            if success:
                self.show_images()

    # Method to apply projection to the image using coordinates specified by the user through the application interface
    def project_image(self):
        points_str = self.points_entry.get()
        if points_str:
            # Convert string of coordinates to a list of tuples
            points_list = [tuple(map(int, point.split(','))) for point in points_str.split()]
            if len(points_list) == 4:
                success = self.image_processor.apply_projection(points_list)
                if success:
                    self.show_images
                else:
                    messagebox.showerror("Error", "Incorrect number of points. It is necessary to specify 4 points.")

# Запуск приложения
if __name__ == "__main__":
    app = App()
    app.mainloop()