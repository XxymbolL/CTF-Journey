package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
	"os"
	"strings"
)

const (
	secretKey = "PEKANRIZZTEK2024"
	flagFile  = "flag.txt" 
)

func pad(data []byte, blockSize int) []byte {
	padding := blockSize - len(data)%blockSize
	padtext := make([]byte, padding)
	for i := range padtext {
		padtext[i] = byte(padding)
	}
	return append(data, padtext...)
}

func unpad(data []byte) []byte {
	length := len(data)
	unpadding := int(data[length-1])
	return data[:(length - unpadding)]
}

func decryptECB(block cipher.Block, data []byte) []byte {
	blockSize := block.BlockSize()
	decrypted := make([]byte, len(data))
	
	for i := 0; i < len(data); i += blockSize {
		block.Decrypt(decrypted[i:i+blockSize], data[i:i+blockSize])
	}
	return unpad(decrypted)
}

func decrypt(ciphertext string) (string, error) {
	decoded, err := hex.DecodeString(ciphertext)
	if err != nil {
		return "", err
	}
	
	block, err := aes.NewCipher([]byte(secretKey))
	if err != nil {
		return "", err
	}
	
	decrypted := decryptECB(block, decoded)
	return string(decrypted), nil
}

func readFlag() string {
	data, err := os.ReadFile(flagFile)
	if err != nil {
		return "Error: Could not read flag file!"
	}
	return string(data)
}

func menu() int {
	fmt.Println("1. Decrypt Message")
	fmt.Println("2. Get Flag")
	fmt.Println("3. Exit")
	fmt.Print(">> ")

	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		return 0
	}
	
	input = strings.TrimSpace(input)
	var choice int
	_, err = fmt.Sscanf(input, "%d", &choice)
	if err != nil {
		return 0
	}
	
	return choice
}

func main() {
	fmt.Println("Welcome to ComVis Selection :>")
	reader := bufio.NewReader(os.Stdin)
	
	for {
		choice := menu()
		switch choice {
		case 1:
			fmt.Print("Enter ciphertext (hex): ")
			ciphertext, _ := reader.ReadString('\n')
			ciphertext = strings.TrimSpace(ciphertext)
			
			decrypted, err := decrypt(ciphertext)
			if err != nil {
				fmt.Println("Invalid ciphertext.")
				continue
			}
			
			fmt.Println("Decrypted:", decrypted)
			
		case 2:
			fmt.Print("Enter the encrypted messages (hex): ")
			ciphertext, _ := reader.ReadString('\n')
			ciphertext = strings.TrimSpace(ciphertext)
			
			decrypted, err := decrypt(ciphertext)
			if err != nil {
				fmt.Println("Invalid ciphertext.")
				continue
			}
			
			if strings.Contains(decrypted, "NETSOS") {
				fmt.Println("Success! Enjoy your flag!")
				flag := readFlag()
				fmt.Println(flag)
				os.Exit(0)
			} else {
				fmt.Println("Invalid message!")
			}
			
		case 3:
			os.Exit(0)
			
		default:
			fmt.Println("Invalid choice!")
		}
	}
}