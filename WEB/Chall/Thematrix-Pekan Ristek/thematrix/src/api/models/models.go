package models

import (
	"github.com/mitchellh/mapstructure"
	"time"
)

type User struct {
	Username    string `json:"username" mapstructure:"username"`
	Description string `json:"description" mapstructure:"description"`
	Private     bool   `json:"private" mapstructure:"private"`
}

type Post struct {
	Author    string    `json:"author" mapstructure:"author"`
	Content   string    `json:"content" mapstructure:"content"`
	CreatedAt time.Time `json:"createdAt" mapstructure:"created_at"`
	Likes     int       `json:"likes" mapstructure:"likes"`
}

func MarshalNodes[T any](object T) map[string]any {
	var m map[string]any
	mapstructure.Decode(object, &m)
	return m
}

func UnmarshalNodes[T any](data map[string]any) T {
	var object T
	mapstructure.Decode(data, &object)
	return object
}
