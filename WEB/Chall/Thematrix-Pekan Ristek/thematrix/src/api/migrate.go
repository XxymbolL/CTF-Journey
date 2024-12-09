package main

import (
	"context"
	"os"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func Migrate(driver neo4j.DriverWithContext) {
	neo4j.ExecuteQuery(
		context.Background(), driver, `
		ALTER DATABASE neo4j SET ACCESS READ ONLY
		`,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	neo4j.ExecuteQuery(
		context.Background(), driver, `
		MATCH (u:User) DETACH DELETE u
		`,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	neo4j.ExecuteQuery(
		context.Background(), driver, `
		MATCH (p:Post) DETACH DELETE p
		`,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	_, err := neo4j.ExecuteQuery(
		context.Background(), driver, `
		CREATE CONSTRAINT IF NOT EXISTS ON (u:User) ASSERT u.username IS UNIQUE
		`,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		panic(err)
	}
	_, err = neo4j.ExecuteQuery(
		context.Background(), driver, `
		CREATE (alice:User {username: "alicechang", description: "Hi, I'm Alice! A software engineer based in Berlin, Germany.", private: false})
		CREATE (bob:User {username: "bobmarley", description: "RC car enthusiast", private: false})
		CREATE (charlie:User {username: "charliebrowne", description: "21 | MLOps | Cloud", private: false})
		CREATE (dave:User {username: "davechase", description: "Austin, TX", private: false})
		CREATE (neo:User {username: "neotheone", description: "I might have the flag...", private: true})

		CREATE (alice_post1:Post {author: "alicechang", content: "Hello, world!", createdAt: datetime("2023-01-01T00:00:00Z"), likes: 1})
		CREATE (alice_post2:Post {author: "alicechang", content: "Testing this out...", createdAt: datetime("2023-01-02T00:00:00Z"), likes: 2})
		CREATE (bob_post1:Post {author: "bobmarley", content: "Got a new RC car today!", createdAt: datetime("2023-01-03T00:00:00Z"), likes: 3})
		CREATE (charlie_post1:Post {author: "charliebrowne", content: "Just got laid off today...", createdAt: datetime("2023-01-04T00:00:00Z"), likes: 0})
		CREATE (dave_post1:Post {author: "davechase", content: "test", createdAt: datetime("2023-01-05T00:00:00Z"), likes: 2})
		CREATE (dave_post2:Post {author: "davechase", content: "wow!", createdAt: datetime("2023-01-05T00:00:00Z"), likes: 1})
		CREATE (neo_post1:Post {author: "neotheone", content: "`+os.Getenv("FLAG")+`", createdAt: datetime("2023-01-06T00:00:00Z"), likes: 0})

		CREATE (alice)-[:POSTED]->(alice_post1)
		CREATE (alice)-[:POSTED]->(alice_post2)
		CREATE (bob)-[:POSTED]->(bob_post1)
		CREATE (charlie)-[:POSTED]->(charlie_post1)
		CREATE (dave)-[:POSTED]->(dave_post1)
		CREATE (neo)-[:POSTED]->(neo_post1)

		CREATE (alice)-[:FOLLOWS]->(charlie)
		CREATE (alice)-[:FOLLOWS]->(neo)
		CREATE (bob)-[:FOLLOWS]->(charlie)
		CREATE (bob)-[:FOLLOWS]->(dave)
		CREATE (charlie)-[:FOLLOWS]->(dave)
		`,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"),
	)
	if err != nil {
		panic(err)
	}
}
