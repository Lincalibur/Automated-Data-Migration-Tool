const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const uploadedInfo = document.getElementById('uploaded-info');
const uploadedName = document.getElementById('uploaded-name');
const convertBtn = document.getElementById('convert-btn');
const convertTo = document.getElementById('convert-to');
const resultBox = document.getElementById('result');

let uploadedFilePath = null;

function showResult(message, isError) {
    resultBox.hidden = false;
    resultBox.textContent = message;
    resultBox.className = 'result ' + (isError ? 'error' : 'success');
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', { method: 'POST', body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                showResult(data.error, true);
                return;
            }
            uploadedFilePath = data.file_path;
            uploadedName.textContent = file.name;
            uploadedInfo.hidden = false;
        })
        .catch((error) => showResult(String(error), true));
}

dropzone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (event) => {
    if (event.target.files.length) uploadFile(event.target.files[0]);
});
dropzone.addEventListener('dragover', (event) => event.preventDefault());
dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    if (files.length) uploadFile(files[0]);
});

convertBtn.addEventListener('click', () => {
    if (!uploadedFilePath) return;
    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: uploadedFilePath, convert_to: convertTo.value }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                showResult(data.error, true);
                return;
            }
            showResult(`Converted successfully: ${data.destination_file}`, false);
        })
        .catch((error) => showResult(String(error), true));
});
