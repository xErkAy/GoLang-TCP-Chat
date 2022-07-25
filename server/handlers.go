package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"net"

	_ "github.com/lib/pq"
)

var db, db_err = sql.Open("postgres", "host=localhost port=5434 user=admin password=admin dbname=golangchat sslmode=disable")

func handleClient(connection net.Conn) {
	defer connection.Close()

	var chat Chat
	var user User

	for {
		data := make([]byte, 4096)
		_, err := connection.Read(data)
		if err != nil {
			break
		}

		json_err := json.Unmarshal(bytes.Trim(data, "'\x00'"), &chat)
		if json_err != nil {
			continue
		}

		if chat.Type == "authorization" {
			if !Authorization(&chat, &user, connection) {
				break
			}
		} else if chat.Type == "registration" {
			Registration(&chat, connection)
			break
		} else if chat.Type == "logout" {
			SendMessage(chat, connection)
			break
		} else if chat.Type == "message" {
			fmt.Println(chat)
			go SendMessage(chat, connection)
		}
	}

	go RemoveUser(user)
}

func SendMessage(chat Chat, connection net.Conn) {
	if chat.Type == "logout" {
		for _, element := range users {
			if element.Connection != connection {
				message := fmt.Sprintf(`{"type": "logoutMessage", "message": { "text": "%s disconnected from the server!" } }`, chat.Username)
				element.Connection.Write([]byte(message))
				fmt.Println(message)
			}
		}
	} else if chat.Message.Reciever == "" {
		for _, element := range users {
			if element.Connection != connection {
				message := fmt.Sprintf(`{"type": "globalMessage", "message": { "text": "%s" } }`, chat.Message.Text)
				element.Connection.Write([]byte(message))
				fmt.Println(message)
			}
		}
	} else {
		for _, element := range users {
			if element.Username == chat.Message.Reciever {
				message := fmt.Sprintf(`{"type": "privateMessage", "message": { "text": "%s", "sender": "%s" } }`, chat.Message.Text, chat.Username)
				element.Connection.Write([]byte(message))
			}
		}
	}
}

func Authorization(chat *Chat, user *User, connection net.Conn) bool {
	response, err := db.Query("SELECT id FROM users WHERE username = $1 AND password = $2", chat.Username, chat.Password)
	if err != nil {
		return false
	}

	defer response.Close()
	if !response.Next() {
		connection.Write([]byte("0"))
		return false
	} else {
		response.Scan(&user.ID)
		user.Username = chat.Username
		user.Connection = connection
		users = append(users, *user)
		connection.Write([]byte("1"))
		return true
	}
}

func Registration(chat *Chat, connection net.Conn) {
	if chat.Username == "" || chat.Password == "" {
		connection.Write([]byte("0"))
		return
	}
	_, err := db.Query("INSERT INTO users(username, password) VALUES ($1, $2)", chat.Username, chat.Password)
	if err != nil {
		connection.Write([]byte("0"))
	} else {
		connection.Write([]byte("1"))
	}
}

func RemoveUser(user User) {
	index := 0

	for i, element := range users {
		if element == user {
			index = i
		}
	}

	if index >= len(users) || index < 0 {
		return
	}

	users = append(users[:index], users[index+1:]...)
}
