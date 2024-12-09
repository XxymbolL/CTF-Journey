package utils

import (
	"encoding/json"
	"strings"
)

func IsDataClean[T any](data T) bool {
	json, err := json.Marshal(data)
	if err != nil {
		return false
	}

	for _, word := range []string{"netsos"} {
		if strings.Contains(strings.ToLower(string(json)), word) {
			return false
		}
	}
	return true
}

func IsInputClean(query string) bool {
	for _, word := range []string{"create", "set", "=", "netsos", "delete", " "} {
		if strings.Contains(strings.ToLower(query), word) {
			return false
		}
	}
	return true
}
