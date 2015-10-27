package main

import (
	"log"
	"net/http"
)

type handler struct {
}

func (h *handler) ServeHTTP(w http.ResponseWriter, _ *http.Request) {
	w.Write([]byte("Hello world!"))
}

func main() {
	log.Fatal(http.ListenAndServe(":8080", &handler{}))
}
