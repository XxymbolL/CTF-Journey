express = require('express')
jwt = require('jsonwebtoken')

app = express()
require('dotenv').config()

app.post('/api/v1/login', (req, res) => {
    // TODO: Implement login
    res.status(401).json({
        message: 'Unauthorized'
    })
})

app.get('/api/v1/flag', (req, res) => {
    token = req.headers.authorization
    split = token.split('Bearer ')
    if (split.length !== 2) {
        res.status(401).json({
            message: 'Unauthorized'
        })
        return
    }

    jwt.verify(split[1], process.env.JWT_SECRET, (err, decoded) => {
        if (err) {
            res.status(401).json({
                message: 'Unauthorized'
            })
            return
        }

        if (decoded.sub !== 'admin') {
            res.status(401).json({
                message: 'Unauthorized'
            })
            return
        }

        res.status(200).json({
            message: process.env.FLAG
        })
    })
})

app.get('/flag', (req, res) => {
    res.sendFile(__dirname + '/templates/flag.html')
})

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/login.html')
})

app.listen(8080, () => {
    console.log('Server is running on port 8080')
})
