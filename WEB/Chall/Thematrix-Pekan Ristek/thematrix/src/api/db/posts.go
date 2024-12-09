package db

import (
	"context"
	"thematrix/models"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func GetPosts(driver neo4j.DriverWithContext, username string) ([]models.Post, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User {username: $username})-[:POSTED]->(p:Post) RETURN p",
		map[string]any{
			"username": username,
		},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return nil, err
	}

	posts := make([]models.Post, 0)
	for _, record := range result.Records {
		data := record.Values[0].(neo4j.Node).Props
		post := models.UnmarshalNodes[models.Post](data)
		posts = append(posts, post)
	}
	return posts, nil
}

func GetAllPosts(driver neo4j.DriverWithContext) ([]models.Post, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User)-[:POSTED]->(p:Post) WHERE u.private = false RETURN p",
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return nil, err
	}

	posts := make([]models.Post, 0)
	for _, record := range result.Records {
		data := record.Values[0].(neo4j.Node).Props
		post := models.UnmarshalNodes[models.Post](data)
		posts = append(posts, post)
	}
	return posts, nil
}
