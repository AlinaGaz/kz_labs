import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

# Класс для обработки изображений
class ImageProcessor:
    def load_image(self, file_path):
        try:
            image = cv2.imread(file_path)
            return image
        except Exception as e:
            print("Error loading image:", e)
            return None

    def display_channel(self, image, channel):
        channel_index = {"Red": 2, "Green": 1, "Blue": 0}.get(channel, 0)
        channel_image = image[:, :, channel_index]
        return channel_image

    def grayscale(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def sepia(self, image):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia_image = cv2.transform(image, kernel)
        return sepia_image

    def brightness_contrast(self, image, brightness=0, contrast=0):
        alpha = (contrast + 100) / 100.0
        beta = brightness
        adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted_image

    def logical_operations(self, image1, image2, operation):
        if operation == "AND":
            result_image = cv2.bitwise_and(image1, image2)
        elif operation == "OR":
            result_image = cv2.bitwise_or(image1, image2)
        elif operation == "XOR":
            result_image = cv2.bitwise_xor(image1, image2)
        elif operation == "NOT":
            result_image = cv2.bitwise_not(image1)
        return result_image

    def hsv_transformation(self, image, hue=0, saturation=0, value=0):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue) % 180
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] + saturation, 0, 255)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + value, 0, 255)
        transformed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return transformed_image

    def median_blur(self, image, kernel_size=3):
        blurred_image = cv2.medianBlur(image, kernel_size)
        return blurred_image

    def window_filter(self, image, kernel):
        filtered_image = cv2.filter2D(image, -1, kernel)
        return filtered_image

    def watercolor(self, image1, image2, brightness=0, contrast=0, blend=0.5):
        adjusted_image = self.brightness_contrast(image1, brightness, contrast)
        blended_image = cv2.addWeighted(adjusted_image, blend, image2, 1 - blend, 0)
        return blended_image

    def cartoon(self, image, threshold=10):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.medianBlur(gray_image, 5)
        edges = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        cartoon_image = cv2.bitwise_and(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), image)
        return cartoon_image

class ImageProcessingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processing Application")

        self.processor = ImageProcessor()

        self.canvas1 = tk.Canvas(self, width=400, height=400)
        self.canvas1.grid(row=0, column=0)

        self.canvas2 = tk.Canvas(self, width=400, height=400)
        self.canvas2.grid(row=0, column=1)

        self.load_button1 = tk.Button(self, text="Load Image 1", command=lambda: self.load_image(1))
        self.load_button1.grid(row=1, column=0)

        self.load_button2 = tk.Button(self, text="Load Image 2", command=lambda: self.load_image(2))
        self.load_button2.grid(row=1, column=1)

        self.apply_button = tk.Button(self, text="Apply", command=self.apply_operation)
        self.apply_button.grid(row=1, column=2)

        self.selected_operation = tk.StringVar()
        self.operation_menu = tk.OptionMenu(self, self.selected_operation, *self.get_operation_list())
        self.operation_menu.grid(row=2, column=0, columnspan=3)

        self.image1 = None
        self.image2 = None
        self.selected_operation.set(self.get_operation_list()[0])

    def load_image(self, image_num):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            image = self.processor.load_image(file_path)
            if image_num == 1:
                self.image1 = image
                self.display_image(self.image1, self.canvas1)
            else:
                self.image2 = image
                self.display_image(self.image2, self.canvas2)

    def apply_operation(self):
        operation = self.selected_operation.get()
        if operation == "Display Channel":
            channel = "Red"  
            processed_image = self.processor.display_channel(self.image1, channel)
        elif operation == "Grayscale":
            processed_image = self.processor.grayscale(self.image1)
        elif operation == "Sepia":
            processed_image = self.processor.sepia(self.image1)
        elif operation == "Brightness and Contrast":
            processed_image = self.processor.brightness_contrast(self.image1, brightness=10, contrast=10)  
        elif operation == "Logical Operations":
            processed_image = self.processor.logical_operations(self.image1, self.image2, "AND")  
        elif operation == "HSV Transformation":
            processed_image = self.processor.hsv_transformation(self.image1, hue=20, saturation=50, value=50)  
        elif operation == "Median Blur":
            processed_image = self.processor.median_blur(self.image1, kernel_size=5)  
        elif operation == "Window Filter":
            kernel = np.ones((3, 3), dtype=np.float32) / 9
            processed_image = self.processor.window_filter(self.image1, kernel)
        elif operation == "Watercolor":
            processed_image = self.processor.watercolor(self.image1, self.image2, brightness=10, contrast=10, blend=0.5)  
        elif operation == "Cartoon":
            processed_image = self.processor.cartoon(self.image1, threshold=10)  
        if processed_image is not None:
            self.display_image(processed_image, self.canvas2)
        else:
            print("Error processing image.")

    def display_image(self, image, canvas):
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(pil_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

    def get_operation_list(self):
        return [
            "Display Channel",
            "Grayscale",
            "Sepia",
            "Brightness and Contrast",
            "Logical Operations",
            "HSV Transformation",
            "Median Blur",
            "Window Filter",
            "Watercolor",
            "Cartoon"
        ]

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.mainloop()
