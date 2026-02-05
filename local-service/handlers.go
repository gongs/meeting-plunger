package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
)

// HealthResponse represents the health check response
type HealthResponse struct {
	Status string `json:"status" example:"healthy"`
}

// TranscriptResponse represents the transcript response
type TranscriptResponse struct {
	Transcript string `json:"transcript" example:"Hello, how are you?"`
}

// ErrorResponse represents an error response
type ErrorResponse struct {
	Error string `json:"error" example:"Method not allowed"`
}

// HandleHealth serves the health check endpoint
// @Summary Health check
// @Description Returns the health status of the client service
// @Tags health
// @Produce json
// @Success 200 {object} HealthResponse
// @Router /health [get]
func HandleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, err := fmt.Fprintf(w, `{"status": "healthy"}`)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}

// HandleTranscribe handles file upload and forwards it to backend
// @Summary Transcribe audio file
// @Description Accepts an audio file and returns its transcription by calling the backend
// @Tags transcription
// @Accept multipart/form-data
// @Produce json
// @Param file formData file true "Audio file to transcribe"
// @Success 200 {object} TranscriptResponse
// @Failure 405 {object} ErrorResponse
// @Router /transcribe [post]
func HandleTranscribe(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse the multipart form
	err := r.ParseMultipartForm(32 << 20) // 32 MB max
	if err != nil {
		http.Error(w, "Error parsing form", http.StatusBadRequest)
		log.Printf("Error parsing form: %v", err)
		return
	}

	// Get the file from the request
	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Error retrieving file", http.StatusBadRequest)
		log.Printf("Error retrieving file: %v", err)
		return
	}
	defer file.Close()

	// Create a buffer to write the multipart form data
	var requestBody bytes.Buffer
	writer := multipart.NewWriter(&requestBody)

	// Create a form file field
	part, err := writer.CreateFormFile("file", handler.Filename)
	if err != nil {
		http.Error(w, "Error creating form file", http.StatusInternalServerError)
		log.Printf("Error creating form file: %v", err)
		return
	}

	// Copy the file content to the form field
	_, err = io.Copy(part, file)
	if err != nil {
		http.Error(w, "Error copying file", http.StatusInternalServerError)
		log.Printf("Error copying file: %v", err)
		return
	}

	// Close the writer to finalize the multipart form
	err = writer.Close()
	if err != nil {
		http.Error(w, "Error closing writer", http.StatusInternalServerError)
		log.Printf("Error closing writer: %v", err)
		return
	}

	// Get backend URL from environment or use default
	backendURL := os.Getenv("BACKEND_URL")
	if backendURL == "" {
		backendURL = "http://localhost:8000"
	}

	// Forward the request to the backend
	req, err := http.NewRequest("POST", backendURL+"/transcribe", &requestBody)
	if err != nil {
		http.Error(w, "Error creating request", http.StatusInternalServerError)
		log.Printf("Error creating request: %v", err)
		return
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	// Send the request to the backend
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, "Error calling backend", http.StatusInternalServerError)
		log.Printf("Error calling backend: %v", err)
		return
	}
	defer resp.Body.Close()

	// Read the response from the backend
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error reading backend response", http.StatusInternalServerError)
		log.Printf("Error reading backend response: %v", err)
		return
	}

	// Verify the response is valid JSON
	var transcriptResp TranscriptResponse
	err = json.Unmarshal(body, &transcriptResp)
	if err != nil {
		http.Error(w, "Invalid response from backend", http.StatusInternalServerError)
		log.Printf("Invalid response from backend: %v", err)
		return
	}

	// Forward the backend response to the client
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	_, err = w.Write(body)
	if err != nil {
		log.Printf("Error writing response: %v", err)
	}
}
