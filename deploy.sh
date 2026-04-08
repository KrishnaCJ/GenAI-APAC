#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validate required environment variables
if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
  echo -e "${RED}Error: GCP_PROJECT_ID is required${NC}"
  echo "Usage: export GCP_PROJECT_ID='your-project-id' && ./deploy.sh"
  exit 1
fi

SERVICE_NAME="${SERVICE_NAME:-farm-guide-agent}"
REGION="${REGION:-asia-south1}"

echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
echo "Project: $GCP_PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"

# Set GCP project
gcloud config set project "$GCP_PROJECT_ID"

# Build and deploy
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10

echo -e "${GREEN}Deployment complete!${NC}"
gcloud run services describe "$SERVICE_NAME" --region "$REGION"
