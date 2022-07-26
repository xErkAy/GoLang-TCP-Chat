package main

import "net"

type Chat struct {
	Username string `json:"username"`
	Type     string `json:"type"`

	Password string `json:"password"`

	ID      int      `json:"id"`
	Message *Message `json:"message"`
	File    *File    `json:"file"`
}

type Message struct {
	Text     string `json:"text"`
	Time     string `json:"time"`
	Reciever string `json:"reciever_username"`
}

type File struct {
	Type     string `json:"type"`
	FileName string `json:"file_name"`
	Data     string `json:"data"`
	Time     string `json:"time"`
	Reciever string `json:"reciever_username"`
}

type User struct {
	ID         int
	Username   string
	Connection net.Conn
}

type SendMessageStruct struct {
	Type   string
	Sender string
}
