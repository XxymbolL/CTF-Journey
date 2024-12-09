package handlers

import (
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

type Handler struct {
	driver neo4j.DriverWithContext
}

func NewHandler(driver neo4j.DriverWithContext) *Handler {
	return &Handler{
		driver: driver,
	}
}
