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
		data := make([]byte, 32768)
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
			LogInOrOut(data, connection)
			break
		} else if chat.Type == "login" {
			go LogInOrOut(data, connection)
		} else if chat.Type == "message" {
			go SendMessage(chat, connection)
		} else if chat.Type == "file_message" {
			go SendFileMessage(chat, connection)
		}
	}

	go RemoveUser(user)
}

func LogInOrOut(data []byte, connection net.Conn) {
	message := string(bytes.Trim(data, "'\x00'"))
	fmt.Println(message)
	for _, element := range users {
		if element.Connection != connection {
			element.Connection.Write([]byte(message))
		}
	}
}

func SendMessage(chat Chat, connection net.Conn) {
	if chat.Message.Reciever == "" {
		message := fmt.Sprintf(`{"username": "%s", "type": "message", "message": {"text": "%s", "time": "%s"}}`, chat.Username, chat.Message.Text, chat.Message.Time)
		fmt.Println(message)
		for _, element := range users {
			if element.Connection != connection {
				element.Connection.Write([]byte(message))
			}
		}
	} else {
		for _, element := range users {
			if element.Username == chat.Message.Reciever {
				element.Connection.Write([]byte(fmt.Sprintf(`{"username": "%s", "type": "private_message", "message": {"text": "%s", "time": "%s"}}`, chat.Username, chat.Message.Text, chat.Message.Time)))
			}
		}
	}
}

func SendFileMessage(chat Chat, connection net.Conn) {
	if chat.File.Type == "file_data" {
		if chat.Message.Reciever == "" {
			message := fmt.Sprintf(`{"username": "%s", "type": "file_data", "file_name": "%s", "data": "%s"}`, chat.Username, chat.File.FileName, chat.File.Data)
			fmt.Println(message)
			for _, element := range users {
				if element.Connection != connection {
					element.Connection.Write([]byte(message))
				}
			}
		} else {
			for _, element := range users {
				if element.Username == chat.File.Reciever {
					element.Connection.Write([]byte(fmt.Sprintf(`{"username": "%s", "type": "private_file_data", "file_name": "%s", "data": "%s"}`, chat.Username, chat.File.FileName, chat.File.Data)))
				}
			}
		}
	} else if chat.File.Type == "end_file_sending" {
		if chat.Message.Reciever == "" {
			message := fmt.Sprintf(`{"username": "%s", "type": "end_file_sending", "file_name": "%s"}`, chat.Username, chat.File.FileName)
			fmt.Println(message)
			for _, element := range users {
				if element.Connection != connection {
					element.Connection.Write([]byte(message))
				}
			}
		} else {
			for _, element := range users {
				if element.Username == chat.Message.Reciever {
					element.Connection.Write([]byte(fmt.Sprintf(`{"username": "%s", "type": "end_file_sending", "file_name": "%s"}`, chat.Username, chat.File.FileName)))
				}
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
