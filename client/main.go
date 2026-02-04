package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	// Parse command line arguments
	if len(os.Args) > 1 && os.Args[1] == "serve" {
		startHTTPServer()
		return
	}

	// CLI mode
	fmt.Println("Meeting Plunger CLI")
	fmt.Println("Usage:")
	fmt.Println("  client serve    Start local HTTP server for browser")
}

func startHTTPServer() {
	http.HandleFunc("/", handleRoot)
	http.HandleFunc("/health", handleHealth)

	port := ":3000"
	fmt.Printf("Starting local HTTP server on http://localhost%s\n", port)
	log.Fatal(http.ListenAndServe(port, nil))
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	fmt.Fprintf(w, `
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
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"status": "healthy"}`)
}
