package db

import (
	"context"
	"thematrix/models"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func GetUser(driver neo4j.DriverWithContext, username string) (models.User, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User {username: \""+username+"\"}) RETURN u",
		map[string]any{
			"username": username,
		},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return models.User{}, err
	}

	if len(result.Records) == 0 {
		return models.User{}, nil
	}

	record := result.Records[0]
	data := record.Values[0].(neo4j.Node).Props
	user := models.UnmarshalNodes[models.User](data)
	return user, nil
}

func GetAllUsers(driver neo4j.DriverWithContext) ([]models.User, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User) RETURN u",
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return nil, err
	}
	if len(result.Records) == 0 {
		return nil, nil
	}

	users := make([]models.User, 0)
	for _, record := range result.Records {
		data := record.Values[0].(neo4j.Node).Props
		user := models.UnmarshalNodes[models.User](data)
		users = append(users, user)
	}
	return users, nil
}

func GetFollowers(driver neo4j.DriverWithContext, username string) ([]models.User, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User {username: $username})<-[:FOLLOWS]-(p:User) RETURN p",
		map[string]any{
			"username": username,
		},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return nil, err
	}

	followers := make([]models.User, 0)
	for _, record := range result.Records {
		data := record.Values[0].(neo4j.Node).Props
		user := models.UnmarshalNodes[models.User](data)
		followers = append(followers, user)
	}
	return followers, nil
}

func GetFollowing(driver neo4j.DriverWithContext, username string) ([]models.User, error) {
	result, err := neo4j.ExecuteQuery(
		context.Background(),
		driver,
		"MATCH (u:User {username: $username})-[:FOLLOWS]->(p:User) RETURN p",
		map[string]any{
			"username": username,
		},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		return nil, err
	}

	followers := make([]models.User, 0)
	for _, record := range result.Records {
		data := record.Values[0].(neo4j.Node).Props
		user := models.UnmarshalNodes[models.User](data)
		followers = append(followers, user)
	}
	return followers, nil
}
