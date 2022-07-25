package main

import (
	"fmt"
	"net"
)

var users = []User{}

func main() {
	if db_err != nil {
		fmt.Printf("Database error: %s", db_err)
		return
	}
	listener, _ := net.Listen("tcp", "localhost:8080")
	for {
		connection, err := listener.Accept()
		if err == nil {
			go handleClient(connection)
		}
	}
}
