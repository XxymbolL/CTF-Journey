given source code and hint
hint: Have you read go documentation for each function I used in this project?


there is some strange user creation logic that The `runMigration()` function creates the admin user if it doesn't already exist:

```go
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
```
this indicate that the FLAG is in the user description field of admin

So what we need here is login as admin
as the CouchDB is given in the source file, Direct database acess might be possible or trying to manipulate the user register or login to acess the admin credential

trying the direct database acess, the request is stuck at waiting
```
GET http://152.118.201.242:5984/users/_all_docs HTTP/1.1
Host: 152.118.201.242:5984
Accept: application/json
Connection: keep-alive
```

there is something also in the admin password, it created with uuid.New().String() which in predictable format

