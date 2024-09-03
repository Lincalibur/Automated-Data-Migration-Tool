import React, { useState } from 'react';

function DragAndDrop() {
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const handleDrop = (event) => {
        event.preventDefault();
        const files = Array.from(event.dataTransfer.files);
        setUploadedFiles(files);

        // Handle file upload to the backend
        files.forEach(file => {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => console.log(data))
              .catch(error => console.error('Error:', error));
        });
    };

    return (
        <div 
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
            style={{ border: '2px dashed #ccc', padding: '20px', textAlign: 'center' }}
        >
            Drag and drop files here
            <ul>
                {uploadedFiles.map((file, index) => (
                    <li key={index}>{file.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default DragAndDrop;
