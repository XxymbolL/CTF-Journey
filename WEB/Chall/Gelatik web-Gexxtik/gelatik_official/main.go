package main

import (
	"context"
	"log"
	"net/http"
	"os"

	"nekoneko/regist/handlers"
	"nekoneko/regist/models"

	"github.com/google/uuid"
)

func runMigration() {
	ctx := context.Background()
	dbClient, err := models.NewDBClient(ctx)
	if err != nil {
		log.Panicf("failed to connect db: %v", err)
	}
	defer dbClient.Close(ctx)

	_, err = dbClient.GetUser(ctx, "admin")
	if err != nil {
		log.Println("User not exist")

		dbClient.CreateUser(ctx, &models.User{
			ID:          uuid.New().String(),
			Username:    "admin",
			Password:    uuid.New().String(),
			Description: os.Getenv("FLAG"),
		})
	}

	log.Println("Migration complete!")
}

func runServer() {
	// Serve static files
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Register routes
	http.HandleFunc("/", handlers.HomeHandler)
	http.HandleFunc("/login", handlers.LoginHandler)
	http.HandleFunc("/register", handlers.RegisterHandler)
	http.HandleFunc("/logout", handlers.LogoutHandler)

	// Start server
	log.Println("Server starting on :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func main() {
	if os.Args[1] == "migrate" {
		runMigration()
	} else {
		runServer()
	}
}
