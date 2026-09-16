// Static demo build: mimics the real app's interactions with fake
// delays and canned responses. No files are read, uploaded, or written.

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const uploadedInfo = document.getElementById('uploaded-info');
const uploadedName = document.getElementById('uploaded-name');
const clearBtn = document.getElementById('clear-btn');
const convertBtn = document.getElementById('convert-btn');
const logList = document.getElementById('log-list');
const statusPill = document.getElementById('status-pill');

const DEMO_DESTINATIONS = {
    pdf_to_word: '.docx',
    sql_to_excel: '.xlsx',
};

let uploadedFileName = null;
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

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function resetUpload() {
    uploadedFileName = null;
    uploadedInfo.hidden = true;
    fileInput.value = '';
    setStatus('idle');
}

function fakeUpload(file) {
    setStatus('uploading', 'busy');
    log('uploading <b>' + escapeHtml(file.name) + '</b>&hellip;', 'info');

    setTimeout(() => {
        uploadedFileName = file.name;
        uploadedName.textContent = file.name;
        uploadedInfo.hidden = false;
        setStatus('ready', 'done');
        log('received <b>' + escapeHtml(file.name) + '</b>, ready to convert <i>(demo &mdash; not actually stored)</i>', 'success');
    }, 500);
}

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        fileInput.click();
    }
});
fileInput.addEventListener('change', (event) => {
    if (event.target.files.length) fakeUpload(event.target.files[0]);
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
    if (files.length) fakeUpload(files[0]);
});

clearBtn.addEventListener('click', () => {
    log('cleared selection', 'info');
    resetUpload();
});

convertBtn.addEventListener('click', () => {
    if (!uploadedFileName) return;
    const selected = document.querySelector('input[name="convert-to"]:checked');
    if (!selected) return;

    convertBtn.disabled = true;
    setStatus('converting', 'busy');
    log('running conversion to <b>' + escapeHtml(selected.value.replace(/_/g, ' ')) + '</b>&hellip;', 'info');

    setTimeout(() => {
        convertBtn.disabled = false;
        const baseName = uploadedFileName.replace(/\.[^.]+$/, '');
        const outName = baseName + (DEMO_DESTINATIONS[selected.value] || '.out');
        setStatus('done', 'done');
        log('done &mdash; <b>' + escapeHtml(outName) + '</b> <i>(demo &mdash; download disabled, grab the real tool to run this locally)</i>', 'success');
    }, 900);
});
