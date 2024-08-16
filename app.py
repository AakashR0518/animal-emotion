import tkinter as tk
from tkinter import filedialog, Label, Button, Frame
from PIL import Image, ImageTk
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained model
model = load_model('initial.h5', compile=False)

# Define class names
class_names = ['angry', 'happy', 'relaxed', 'sad']

# Create the main application window
root = tk.Tk()
root.title("Animal Emotion Classifier")
root.geometry("600x500")
root.configure(bg="#2e3f4f")
content_frame = Frame(root, bg="#2e3f4f")
content_frame.pack(pady=20)

# Function to load and preprocess the selected image
def classify_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Load and preprocess the image
    img = image.load_img(file_path, target_size=(384, 384))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 1./255.0  # Normalize to [0, 1]

    # Make a prediction
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=-1)
    predicted_class_name = class_names[predicted_class_index[0]]

    # Display the prediction
    result_label.config(text=f"Predicted class: {predicted_class_name}")

    # Display the selected image in the GUI
    img = Image.open(file_path)
    img.thumbnail((250, 250))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

# GUI elements
image_label = Label(content_frame, bg="#2e3f4f", relief="solid", bd=2)
image_label.grid(row=0, column=0, padx=20, pady=20)

result_label = Label(content_frame, text="Select an image to classify", font=("Comic Sans", 14, "bold"), fg="#ffffff", bg="#2e3f4f")
result_label.grid(row=0, column=1, padx=20)

def on_enter(e):
    classify_button['background'] = '#405a7a'
def on_leave(e):
    classify_button['background'] = '#4a678e'

classify_button = Button(root, text="Select Image", command=classify_image, font=("Comic Sans", 14, "bold"), fg="#ffffff", bg="#4a678e", activebackground="#405a7a", padx=10, pady=5, bd=0, cursor="hand2")
classify_button.pack(pady=20)
classify_button.bind("<Enter>", on_enter)
classify_button.bind("<Leave>", on_leave)

# Start the application
root.mainloop()