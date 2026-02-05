.PHONY: test lint format

test:
	@echo "Running Go tests..."
	@go test -v ./...

lint:
	@echo "Running Go linters..."
	@golangci-lint run ./...

format:
	@echo "Formatting Go code..."
	@gofmt -w -s .
	@goimports -w .
