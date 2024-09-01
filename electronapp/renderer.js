const axios = require('axios');
const path = require('path');
console.log("Started");

function displayImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (file) {
        const imageUrl = URL.createObjectURL(file);
        const selectedImage = document.getElementById('selectedImage');
        selectedImage.src = imageUrl;
        selectedImage.style.display = 'block';
    }
}

function classifyImage() {
    console.log("Button clicked!");
    const fileInput = document.getElementById('fileInput');
    console.log("File input element:", fileInput);
    if (fileInput.files.length === 0) {
        alert('Please select an image file.');
        return;
    }
    const file = fileInput.files[0];

    const filePath = fileInput.files[0].path;
    console.log("Selected file path:", filePath);

    const formData = new FormData();
    formData.append('file', file);
    
    axios.post('http://127.0.0.1:5000/predict', {
        img_path: filePath
    })
    .then(response => {
        const resultDiv = document.getElementById('result');
        resultDiv.textContent = `Predicted Class: ${response.data.predicted_class}`;
        localStorage.setItem('result', response.data.predicted_class);
    })
    .catch(error => {
        console.error(error);
        alert('Error classifying image.');
    });

    document.getElementById('nextButton').style.display = 'block';
}

function navigateToInputScreen() {
    window.location.href = 'input.html';
}

document.getElementById('nextButton').addEventListener('click', navigateToInputScreen);

function saveInputValues() {
    const diet = document.getElementById('diet').value;
    const sleep = document.getElementById('sleep').value;
    const behavior = document.getElementById('behavior').value;

    localStorage.setItem('diet', diet);
    localStorage.setItem('sleep', sleep);
    localStorage.setItem('behavior', behavior);
}

async function fetchAndDisplayAdvice() {

    const diet = String(localStorage.getItem('diet'));
    const sleep = String(localStorage.getItem('sleep'));
    const behavior = String(localStorage.getItem('behavior'));

    const dogInfo = { diet, sleep, behavior };
    console.log(dogInfo)

    const imageResult = String(localStorage.getItem('result'));

    console.log('Sending Data:', { dogInfo, imageResult})
    

    axios.post('http://127.0.0.1:5000/generate_advice', {
        dogInfo,
        imageResult
    })
    .then(response => {
        const advice = response.data.advice.replace(/\n/g, '<br>');
        console.log("Received advice:", advice);

        document.getElementById('adviceText').innerHTML = advice;

        document.getElementById('adviceScreen').style.display = 'block';
    })
    .catch(error => {
        console.error('Error fetching advice:', error);
        document.getElementById('adviceText').textContent = 'Sorry, we could not generate advice at this time.';
    });
    document.getElementById('submitDogInfoButton').style.display = 'block'
}

function navigateToAdviceScreen() {
    window.location.href = 'advice.html';
}

document.getElementById('submitDogInfoButton').addEventListener('click', navigateToAdviceScreen);