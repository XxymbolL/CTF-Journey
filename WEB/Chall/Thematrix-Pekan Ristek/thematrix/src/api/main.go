package main

import (
	"context"
	"log"
	"os"
	"thematrix/handlers"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	driver, err := neo4j.NewDriverWithContext(
		os.Getenv("NEO4J_TARGET_URL"),
		neo4j.BasicAuth(
			os.Getenv("NEO4J_USERNAME"),
			os.Getenv("NEO4J_PASSWORD"),
			"",
		),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer driver.Close(context.Background())

	router.Use(cors.New(cors.Config{
		AllowOrigins:  []string{"http://localhost:3000"},
		AllowMethods:  []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:  []string{"Origin", "Content-Length", "Content-Type"},
		ExposeHeaders: []string{"Content-Length"},
		MaxAge:        300,
	}))

	handler := handlers.NewHandler(driver)

	router.GET("/api/users/followers", handler.GetFollowers)
	router.GET("/api/users/following", handler.GetFollowing)
	router.GET("/api/users", handler.GetUsers)
	router.GET("/api/posts", handler.GetPosts)

	Migrate(driver)
	router.Run(":8080")
}
