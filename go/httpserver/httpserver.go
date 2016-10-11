package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", server)
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func server(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Simple http server")
}
