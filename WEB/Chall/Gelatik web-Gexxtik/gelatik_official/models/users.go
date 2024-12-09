package models

import (
	"context"
	"fmt"
	"os"
	"time"

	_ "github.com/go-kivik/couchdb/v3" // The CouchDB driver
	"github.com/go-kivik/kivik/v3"
)

type User struct {
	ID          string    `json:"_id,omitempty"`
	Rev         string    `json:"_rev,omitempty"`
	Username    string    `json:"username"`
	Password    string    `json:"password"`
	Description string    `json:"description"`
	CreatedAt   time.Time `json:"created_at"`
}

type DBClient struct {
	client *kivik.Client
	db     *kivik.DB
}

// Initialize CouchDB connection
func NewDBClient(ctx context.Context) (*DBClient, error) {
	// Connect to CouchDB
	dburl := "http://localhost:5984/"
	if os.Getenv("DB_URL") != "" {
		dburl = os.Getenv("DB_URL")
	}
	client, err := kivik.New("couch", dburl)
	if err != nil {
		return nil, fmt.Errorf("failed to create client: %w", err)
	}

	// Create or connect to database
	isDbExist, _ := client.DBExists(ctx, "users")
	if !isDbExist {
		if err := client.CreateDB(ctx, "users"); err != nil {
			return nil, fmt.Errorf("failed to create database: %w", err)
		}
	}

	db := client.DB(ctx, "users")
	if db.Err() != nil {
		// If database doesn't exist, create it
		if err := client.CreateDB(ctx, "users"); err != nil {
			return nil, fmt.Errorf("failed to create database: %w", err)
		}
		db = client.DB(ctx, "users")
	}

	return &DBClient{
		client: client,
		db:     db,
	}, nil
}

func (c *DBClient) CreateUser(ctx context.Context, user *User) error {
	user.CreatedAt = time.Now()
	rev, err := c.db.Put(ctx, user.ID, user)
	if err != nil {
		return fmt.Errorf("failed to create document: %w", err)
	}
	user.Rev = rev
	return nil
}

func (c *DBClient) GetUser(ctx context.Context, username string) (User, error) {
	var user User

	query := map[string]interface{}{
		"selector": map[string]interface{}{
			"username": username,
		},
		"limit": 1,
	}

	row, err := c.db.Find(ctx, query)
	if err != nil {
		return user, fmt.Errorf("failed to execute query: %w", err)
	}
	defer row.Close()

	if !row.Next() {
		return user, fmt.Errorf("failed to scan document: %w", err)
	}

	if err := row.ScanDoc(&user); err != nil {
		return user, fmt.Errorf("failed to scan document: %w", err)
	}
	return user, nil
}

func (c *DBClient) Close(ctx context.Context) {
	c.db.Close(ctx)
	c.client.Close(ctx)
}
