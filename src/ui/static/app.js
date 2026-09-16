const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const uploadedInfo = document.getElementById('uploaded-info');
const uploadedName = document.getElementById('uploaded-name');
const clearBtn = document.getElementById('clear-btn');
const convertBtn = document.getElementById('convert-btn');
const logList = document.getElementById('log-list');
const statusPill = document.getElementById('status-pill');

let uploadedFilePath = null;
let bootLogCleared = false;

function timestamp() {
    return new Date().toLocaleTimeString('en-GB', { hour12: false });
}

function log(message, kind) {
    if (!bootLogCleared) {
        logList.innerHTML = '';
        bootLogCleared = true;
    }
    const entry = document.createElement('li');
    entry.className = 'log-entry log-entry-' + (kind || 'info');

    const time = document.createElement('span');
    time.className = 'log-time';
    time.textContent = '[' + timestamp() + ']';

    const msg = document.createElement('span');
    msg.className = 'log-msg';
    msg.innerHTML = message;

    entry.append(time, msg);
    logList.appendChild(entry);
    logList.scrollTop = logList.scrollHeight;
}

function setStatus(text, kind) {
    statusPill.textContent = text;
    statusPill.className = kind || '';
}

function resetUpload() {
    uploadedFilePath = null;
    uploadedInfo.hidden = true;
    fileInput.value = '';
    setStatus('idle');
}

function uploadFile(file) {
    setStatus('uploading', 'busy');
    log('uploading <b>' + escapeHtml(file.name) + '</b>&hellip;', 'info');

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', { method: 'POST', body: formData })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                setStatus('error', 'busy');
                log(escapeHtml(data.error), 'error');
                return;
            }
            uploadedFilePath = data.file_path;
            uploadedName.textContent = file.name;
            uploadedInfo.hidden = false;
            setStatus('ready', 'done');
            log('received <b>' + escapeHtml(file.name) + '</b>, ready to convert', 'success');
        })
        .catch((error) => {
            setStatus('error', 'busy');
            log(escapeHtml(String(error)), 'error');
        });
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        fileInput.click();
    }
});
fileInput.addEventListener('change', (event) => {
    if (event.target.files.length) uploadFile(event.target.files[0]);
});
dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropzone.classList.add('dragging');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragging'));
dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropzone.classList.remove('dragging');
    const files = Array.from(event.dataTransfer.files);
    if (files.length) uploadFile(files[0]);
});

clearBtn.addEventListener('click', () => {
    log('cleared selection', 'info');
    resetUpload();
});

convertBtn.addEventListener('click', () => {
    if (!uploadedFilePath) return;
    const selected = document.querySelector('input[name="convert-to"]:checked');
    if (!selected) return;

    convertBtn.disabled = true;
    setStatus('converting', 'busy');
    log('running conversion to <b>' + escapeHtml(selected.value.replace(/_/g, ' ')) + '</b>&hellip;', 'info');

    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: uploadedFilePath, convert_to: selected.value }),
    })
        .then((response) => response.json())
        .then((data) => {
            convertBtn.disabled = false;
            if (data.error) {
                setStatus('error', 'busy');
                log(escapeHtml(data.error), 'error');
                return;
            }
            const filename = data.destination_file.split(/[\\/]/).pop();
            setStatus('done', 'done');
            log('done &mdash; <a href="/output_files/' + encodeURIComponent(filename) + '">' + escapeHtml(filename) + '</a>', 'success');
        })
        .catch((error) => {
            convertBtn.disabled = false;
            setStatus('error', 'busy');
            log(escapeHtml(String(error)), 'error');
        });
});
