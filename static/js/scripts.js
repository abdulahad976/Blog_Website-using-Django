// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    var images = [
        "/static/images/image5.jpeg",
        "/static/images/image6.jpeg",
        "/static/images/image7.jpeg"
        // Add more image paths as needed
    ];

    var currentIndex = 0;
    var imgElement = document.getElementById('transition-image');

    setInterval(function() {
        imgElement.src = images[currentIndex];
        currentIndex = (currentIndex + 1) % images.length;
    }, 1500); // Change the interval (in milliseconds) as desired
});
