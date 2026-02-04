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
		</head>
		<body>
			<h1>Meeting Plunger</h1>
			<p>Local client interface</p>
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
