FROM golang:1.23-alpine

WORKDIR /app
RUN mkdir logs
COPY . .
RUN go build -o app
RUN echo "flagtest" > /flag.txt

CMD ["./app"]