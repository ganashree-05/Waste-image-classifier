console.log("🔥 script.js loaded successfully");

// Preview image before upload
function previewImage(event) {
    let file = event.target.files[0];

    if (!file) return;

    let reader = new FileReader();

    reader.onload = function () {
        let img = document.getElementById("preview");
        if (img) {
            img.src = reader.result;
            img.style.display = "block";
        }
    };

    reader.readAsDataURL(file);
}

// Predict waste image
function predictWaste() {

    console.log("🚀 predictWaste() called");

    let fileInput = document.getElementById("fileInput");

    if (!fileInput) {
        console.log("❌ fileInput not found in HTML");
        return;
    }

    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    // UI loading state
    let classBox = document.getElementById("class");
    let confBox = document.getElementById("confidence");
    let dispoBox = document.getElementById("disposal");

    if (classBox) classBox.innerText = "Processing...";
    if (confBox) confBox.innerText = "--";
    if (dispoBox) dispoBox.innerText = "--";

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        console.log("📡 Response status:", response.status);
        return response.json();
    })
    .then(data => {

        console.log("📦 Server response:", data);

        if (data.error) {
            alert("Error from backend: " + data.error);
            return;
        }

        if (classBox) classBox.innerText = data.class || "N/A";
        if (confBox) confBox.innerText = (data.confidence || 0) + "%";
        if (dispoBox) dispoBox.innerText = data.disposal || "N/A";
    })
    .catch(error => {
        console.log("❌ Fetch error:", error);
        alert("Backend not responding. Check Flask server.");
    });
}