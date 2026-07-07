# --- Stage 1: Build Stage ---
FROM golang:1.22-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy go.mod and go.sum first (if they exist) to leverage Docker cache
# For this basic example, we will just copy the source code directly
COPY main.go .

# Compile the application:
# - CGO_ENABLED=0 disables dynamic C libraries (required for scratch/distroless)
# - GOOS=linux ensures it compiles for Linux architecture
# - ldflags "-s -w" strips debug information and symbols to shrink the binary further
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o myservice main.go

# --- Stage 2: Final Minimal Stage ---
# You can use 'gcr.io/distroless/static-debian12' or 'scratch'
FROM scratch

# Copy the compiled binary from the builder stage
COPY --from=builder /app/myservice /myservice

# Expose the port the app runs on
EXPOSE 8080

# Run the binary
ENTRYPOINT ["/myservice"]
