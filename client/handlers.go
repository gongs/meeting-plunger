package main

import (
	"fmt"
	"log"
	"net/http"
)

// HandleRoot serves the root page
func HandleRoot(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	_, err := fmt.Fprintf(w, `
		<!DOCTYPE html>
		<html>
		<head>
			<title>Meeting Plunger</title>
			<style>
				body {
					font-family: system-ui, -apple-system, sans-serif;
					max-width: 800px;
					margin: 0 auto;
					padding: 20px;
				}
				.upload-form {
					margin: 20px 0;
					padding: 20px;
					border: 1px solid #ccc;
					border-radius: 8px;
				}
				button {
					background-color: #0066cc;
					color: white;
					padding: 10px 20px;
					border: none;
					border-radius: 4px;
					cursor: pointer;
					font-size: 16px;
				}
				button:hover {
					background-color: #0052a3;
				}
				#result {
					margin-top: 20px;
					padding: 15px;
					background-color: #f5f5f5;
					border-radius: 4px;
					display: none;
				}
			</style>
		</head>
		<body>
			<h1>Meeting Plunger</h1>
			<p>Convert audio recordings to transcript</p>
			
			<div class="upload-form">
				<h2>Upload Audio File</h2>
				<form id="uploadForm">
					<input type="file" id="audioFile" accept="audio/*" required>
					<br><br>
					<button type="submit">Upload</button>
				</form>
			</div>
			
			<div id="result"></div>
			
			<script>
				document.getElementById('uploadForm').addEventListener('submit', async (e) => {
					e.preventDefault();
					
					const fileInput = document.getElementById('audioFile');
					const resultDiv = document.getElementById('result');
					
					if (!fileInput.files.length) {
						alert('Please select a file');
						return;
					}
					
					const formData = new FormData();
					formData.append('file', fileInput.files[0]);
					
					try {
						const response = await fetch('/upload', {
							method: 'POST',
							body: formData
						});
						
					const data = await response.json();
					resultDiv.textContent = data.transcript;
					resultDiv.style.display = 'block';
					} catch (error) {
						resultDiv.textContent = 'Error: ' + error.message;
						resultDiv.style.display = 'block';
					}
				});
			</script>
		</body>
		</html>
	`)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}

// HandleHealth serves the health check endpoint
func HandleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, err := fmt.Fprintf(w, `{"status": "healthy"}`)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}

// HandleUpload handles file upload and returns hardcoded transcription
func HandleUpload(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// TODO: Process the uploaded file and call backend API
	// For now, return hardcoded response
	w.Header().Set("Content-Type", "application/json")
	_, err := fmt.Fprintf(w, `{"transcript": "Hello, how are you?"}`)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}
