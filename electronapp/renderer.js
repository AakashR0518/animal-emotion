const axios = require('axios');
const path = require('path');
console.log("Started");

function displayImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (file) {
        // Create a URL for the selected image and display it
        const imageUrl = URL.createObjectURL(file);
        const selectedImage = document.getElementById('selectedImage');
        selectedImage.src = imageUrl;
        selectedImage.style.display = 'block'; // Show the image
    }
}

function classifyImage() {
    console.log("Button clicked!");  // Check if this logs when the button is pressed
    const fileInput = document.getElementById('fileInput');
    console.log("File input element:", fileInput);
    if (fileInput.files.length === 0) {
        alert('Please select an image file.');
        return;
    }
    const file = fileInput.files[0];

    const filePath = fileInput.files[0].path;
    console.log("Selected file path:", filePath);  // Check if this shows the correct path

    const formData = new FormData();
    formData.append('file', file);
    
    axios.post('http://127.0.0.1:5000/predict', {
        img_path: filePath
    })
    .then(response => {
        const resultDiv = document.getElementById('result');
        resultDiv.textContent = `Predicted Class: ${response.data.predicted_class}`;
    })
    .catch(error => {
        console.error(error);  // Log any errors that occur during the request
        alert('Error classifying image.');
    });
}
