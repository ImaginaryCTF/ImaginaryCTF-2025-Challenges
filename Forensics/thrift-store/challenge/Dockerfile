# Stage 1: Build stage
FROM golang:1.24-alpine AS build

# Set the working directory
WORKDIR /app

# Copy and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux go build -o store .

# Stage 2: Final stage
FROM gcr.io/distroless/static AS final
# Set the working directory
WORKDIR /app

# Copy the binary from the build stage
COPY --from=build /app/store .

EXPOSE 9090
# Set the entrypoint command
ENTRYPOINT ["/app/store"]