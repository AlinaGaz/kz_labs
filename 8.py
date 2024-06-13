import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Функция для чтения изображений и их меток из заданной директории
def get_images(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    images = []
    labels = []
    for image_path in image_paths:
        image = Image.open(image_path).convert('L')
        images.append(np.array(image))
        # Извлекаем метку из имени файла
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        label = 0  # Метка по умолчанию
        split_name = file_name.split("subject")
        if len(split_name) > 1:
            label = int(split_name[1])
        labels.append(label)
    return images, labels


# Function to detect and display faces on the image
def recognize_and_display_face(image, image_path, output_path):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Display the original image
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(image_path))[0] + '_processed.jpg')
    plt.savefig(output_file)
    plt.close(fig)

# Path to the Haar cascade file for face detection
cascadePath = r"C:\Users\song_\Downloads\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Path to the directory with training images
input_path = r'C:\Users\song_\Downloads\faces'

# Get images and their labels for training
images, labels = get_images(input_path)
print("Training started...")

# Train the recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))
print("Training completed. The program successfully detected faces in the image.")

# Path to the directory where processed images will be saved
output_path = r'C:\Users\song_\Downloads\КЗ 211-172 Газизова Алина Андреевна лабы\8'

# Create the directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Display processed images
for image_path in os.listdir(input_path):
    if image_path.endswith('.jpg'):
        image = cv2.imread(os.path.join(input_path, image_path))
        recognize_and_display_face(image, image_path, output_path)

print("The program processed all images in the directory and saved them with the _processed.jpg suffix in the recognized_faces folder.")
