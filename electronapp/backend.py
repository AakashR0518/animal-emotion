from flask import Flask, request, jsonify
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import google.generativeai as genai
import os


genai.configure(api_key='AIzaSyC4z8RjUqmf7jso4TkL4TTRVeCELGRhzwA')

app = Flask(__name__)

class_names = ['Angry', 'Happy', 'Relaxed', 'Sad']

model = load_model('initial.h5',compile=False)

@app.route('/predict', methods=['POST'])
def predict():
    img_path = request.json['img_path']
    if not os.path.exists(img_path):
        return jsonify({'error': 'File not found'}), 400
    
    img = image.load_img(img_path, target_size=(384, 384))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 1./255.0

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=-1)
    predicted_class_name = class_names[predicted_class_index[0]]

    return jsonify({'predicted_class': predicted_class_name})
    pass

@app.route('/generate_advice', methods=['POST'])
def generate_advice():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.json

        dog_info = data.get('dogInfo', {})
        image_result = data.get('imageResult', '')

        diet = dog_info.get('diet', 'unknown')
        sleep = dog_info.get('sleep', 'unknown')
        behavior = dog_info.get('behavior', 'unknown')

        prompt = f'''
        Given the following details about a dog:
        Diet: {diet}
        Sleep Schedule: {sleep}
        Behavioral Patterns: {behavior}
        Current Emotion (from image): {image_result}

        Provide personalized advice on how to keep this dog healthy and happy in a list format, please be straightforward, detailed, and provide no introductions:'''

        response = model.generate_content(prompt)

        try:
            advice = response.candidates[0].content.parts[0].text.strip()
        except (AttributeError, IndexError) as e:
            advice = 'No advice generated.'
            print(f"Error extracting advice: {e}")

        return jsonify({'advice': advice})

    except Exception as e:
        print(f"Error generating advice: {e}")
        return jsonify({'error': 'Failed to generate advice'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
