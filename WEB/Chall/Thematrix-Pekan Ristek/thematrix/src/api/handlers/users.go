package handlers

import (
	"thematrix/db"
	"thematrix/utils"

	"github.com/gin-gonic/gin"
)

func (h *Handler) GetUsers(c *gin.Context) {
	username := c.Query("username")
	if !utils.IsInputClean(username) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}
	if username == "" {
		users, err := db.GetAllUsers(h.driver)
		if err != nil {
			c.JSON(500, gin.H{
				"error": err.Error(),
			})
			return
		}
		c.JSON(200, gin.H{
			"data": users,
		})
		return
	}

	user, err := db.GetUser(h.driver, username)
	if err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}
	if !utils.IsDataClean(user) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}

	c.JSON(200, gin.H{
		"data": user,
	})
}

func (h *Handler) GetFollowers(c *gin.Context) {
	username := c.Query("username")
	if !utils.IsInputClean(username) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}
	if username == "" {
		c.JSON(400, gin.H{
			"error": "username is required",
		})
		return
	}

	users, err := db.GetFollowers(h.driver, username)
	if err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"data": users,
	})
}

func (h *Handler) GetFollowing(c *gin.Context) {
	username := c.Query("username")
	if !utils.IsInputClean(username) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}
	if username == "" {
		c.JSON(400, gin.H{
			"error": "username is required",
		})
		return
	}

	users, err := db.GetFollowing(h.driver, username)
	if err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"data": users,
	})
}
