#!/bin/bash

# Load environment variables
source .env

# Build Docker image
docker build -t localgpt .

# Run Docker container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -e EXA_API_KEY="$EXA_API_KEY" \
  -e MODEL_TYPE="$MODEL_TYPE" \
  localgpt