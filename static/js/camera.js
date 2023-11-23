// // Static script to be included in the base HTML template
// // FaceRecognitionDoorbell/static/js/camera.js

// navigator.mediaDevices.getUserMedia({ video: true })
//     .then(stream => {
//         document.querySelector('#video').srcObject = stream;
//     })
//     .catch(error => {
//         console.error("Error accessing the webcam", error);
//     });

// function captureImage() {
//     const video = document.querySelector('#video');
//     const canvas = document.createElement('canvas');
//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;
//     canvas.getContext('2d').drawImage(video, 0, 0);
    
//     // Convert canvas to data URL
//     const dataUrl = canvas.toDataURL('image/jpeg');
    
//     // We can either send this to the server directly via JavaScript
//     // or set it as the value of a hidden input field in a form.
// }
