package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const (
	// Maximum memory allocated for parsing the multipart form
	maxMemory = 32 << 20 // 32MB
	// Directory to save uploaded files
	uploadDir = "./uploads"
)

func handleFileUpload(w http.ResponseWriter, r *http.Request) {
	// Ensure the upload directory exists
	if err := os.MkdirAll(uploadDir, 0755); err != nil {
		http.Error(w, "Failed to create upload directory", http.StatusInternalServerError)
		return
	}

	// Parse the multipart form with memory limit
	if err := r.ParseMultipartForm(maxMemory); err != nil {
		http.Error(w, "Failed to parse multipart form", http.StatusBadRequest)
		return
	}
	defer r.MultipartForm.RemoveAll()

	// Get the file headers from the form
	files := r.MultipartForm.File["files"]
	if len(files) == 0 {
		http.Error(w, "No files uploaded", http.StatusBadRequest)
		return
	}

	// Process each uploaded file
	for i, fileHeader := range files {
		// Open the uploaded file
		uploadedFile, err := fileHeader.Open()
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to open file %s: %v", fileHeader.Filename, err), 
				http.StatusInternalServerError)
			return
		}
		defer uploadedFile.Close()

		// Create a destination file
		dstPath := filepath.Join(uploadDir, fileHeader.Filename)
		dst, err := os.Create(dstPath)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to create destination file: %v", err), 
				http.StatusInternalServerError)
			return
		}
		defer dst.Close()

		// Stream the file to disk using a buffer
		if _, err := io.Copy(dst, uploadedFile); err != nil {
			http.Error(w, fmt.Sprintf("Failed to save file %s: %v", fileHeader.Filename, err), 
				http.StatusInternalServerError)
			return
		}

		fmt.Printf("Successfully saved file %d: %s\n", i+1, fileHeader.Filename)
	}

	fmt.Fprintf(w, "Successfully uploaded %d files\n", len(files))
}

func main() {
	// Register the upload handler
	http.HandleFunc("/upload", handleFileUpload)

	// Start the server
	port := ":8080"
	fmt.Printf("Server starting on port %s...\n", port)
	if err := http.ListenAndServe(port, nil); err != nil {
		fmt.Printf("Server failed to start: %v\n", err)
	}
}
