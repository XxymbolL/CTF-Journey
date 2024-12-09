package handlers

import (
	"thematrix/db"
	"thematrix/utils"

	"github.com/gin-gonic/gin"
)

func (h *Handler) GetPosts(c *gin.Context) {
	username := c.Query("username")
	if !utils.IsInputClean(username) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}
	if username == "" {
		posts, err := db.GetAllPosts(h.driver)
		if err != nil {
			c.JSON(500, gin.H{
				"error": err.Error(),
			})
			return
		}
		if !utils.IsDataClean(posts) {
			c.JSON(400, gin.H{
				"error": "Invalid payload",
			})
			return
		}
		c.JSON(200, gin.H{
			"data": posts,
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
	if user.Private {
		c.JSON(401, gin.H{
			"error": "User is private",
		})
		return
	}
	posts, err := db.GetPosts(h.driver, username)
	if err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}
	if !utils.IsDataClean(posts) {
		c.JSON(400, gin.H{
			"error": "Invalid payload",
		})
		return
	}

	c.JSON(200, gin.H{
		"data": posts,
	})
}
