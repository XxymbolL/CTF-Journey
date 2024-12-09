# Stage 1: Build the Go binary
FROM golang:1.23 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy go.mod and go.sum files to the workspace
COPY go.mod go.sum ./

# Download the Go modules
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o myapp

# Stage 2: Create a lightweight image to run the binary
FROM alpine:latest

# Install necessary certificates
RUN apk --no-cache add ca-certificates

# Set the working directory for the runtime
WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/myapp .
COPY startup.sh .
COPY templates templates
RUN chmod +x startup.sh
RUN mkdir static && chmod -R 777 static

# Expose any necessary ports (if applicable)
EXPOSE 8080

# Command to run the binary
CMD ["./startup.sh"]
