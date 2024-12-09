package handlers

import (
	"context"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"

	"nekoneko/regist/models"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

var templates = template.Must(template.ParseGlob("templates/*.html"))

func GetGravatarImage(uid string, url string) {
	checker := NewBlacklistChecker()
	isBlacklisted, err := checker.IsBlacklisted(url)
	if err != nil {
		log.Printf("Error checking %s: %v\n", url, err)
		return
	}
	if isBlacklisted {
		log.Printf("Blacklisting %s\n", url)
		return
	}

	res, err := http.Get(url)
	if err != nil {
		log.Println(err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		log.Printf("Response failed with status code: %d\n", res.StatusCode)
	}

	// Create the file
	file, err := os.Create(fmt.Sprintf("static/%s.png", uid))
	if err != nil {
		log.Printf("failed to create file: %v", err)
		return
	}
	defer file.Close()

	_, err = io.Copy(file, res.Body)
	if err != nil {
		log.Printf("failed to write file: %v", err)
		return
	}
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}
	http.Redirect(w, r, "/login", http.StatusSeeOther)
}

func LoginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		templates.ExecuteTemplate(w, "login.html", nil)
		return
	}

	if r.Method == "POST" {
		// Initialize client
		ctx := context.Background()
		dbClient, err := models.NewDBClient(ctx)
		if err != nil {
			log.Fatalf("Failed to initialize DB client: %v", err)
		}
		defer dbClient.Close(ctx)

		username := r.FormValue("username")
		password := r.FormValue("password")

		user, err := dbClient.GetUser(ctx, username)
		if err != nil {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password))
		if err != nil {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		fmt.Println(templates.ExecuteTemplate(w, "profile.html", user))
	}
}

func RegisterHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		templates.ExecuteTemplate(w, "register.html", nil)
		return
	}

	if r.Method == "POST" {
		// Initialize client
		ctx := context.Background()
		dbClient, err := models.NewDBClient(ctx)
		if err != nil {
			log.Fatalf("Failed to initialize DB client: %v", err)
		}
		defer dbClient.Close(ctx)

		username := r.FormValue("username")
		password := r.FormValue("password")
		confirm_password := r.FormValue("confirm_password")
		gravatar_url := r.FormValue("gravatar_url")

		if confirm_password != password {
			http.Error(w, "Password is not equal", http.StatusBadRequest)
			return
		}

		_, err = dbClient.GetUser(ctx, username)
		if err == nil {
			http.Error(w, "Username already exists", http.StatusBadRequest)
			return
		}

		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
		if err != nil {
			http.Error(w, "Internal server error", http.StatusInternalServerError)
			return
		}

		user := &models.User{
			ID:          uuid.New().String(),
			Username:    username,
			Password:    string(hashedPassword),
			Description: "",
		}

		err = dbClient.CreateUser(ctx, user)
		if err != nil {
			fmt.Println(err)
			http.Error(w, "Internal server error", http.StatusInternalServerError)
			return
		}
		GetGravatarImage(user.ID, gravatar_url)

		http.Redirect(w, r, "/login", http.StatusSeeOther)
	}
}

func LogoutHandler(w http.ResponseWriter, r *http.Request) {
	http.SetCookie(w, &http.Cookie{
		Name:   "username",
		Value:  "",
		Path:   "/",
		MaxAge: -1,
	})
	http.Redirect(w, r, "/login", http.StatusSeeOther)
}
