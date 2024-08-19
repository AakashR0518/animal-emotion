from flask import Flask, request, jsonify
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image

app = Flask(__name__)

class_names = ['Angry', 'Happy', 'Relaxed', 'Sad']

model = load_model('initial.h5',compile=False)

@app.route('/predict', methods=['POST'])
def predict():
    img_path = request.json['img_path']
    if not os.path.exists(img_path):
        return jsonify({'error': 'File not found'}), 400
    
    img = image.load_img(img_path, target_size=(384, 384))  # Adjust target_size to your model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 1./255.0  # Normalize if required by your model

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=-1)
    predicted_class_name = class_names[predicted_class_index[0]]

    return jsonify({'predicted_class': predicted_class_name})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
