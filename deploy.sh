#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
  echo "GCP_PROJECT_ID is required"
  exit 1
fi

SERVICE_NAME=${SERVICE_NAME:-farm-guide-agent}
REGION=${REGION:-asia-south1}

if [[ -z "${GOOGLE_API_KEY:-}" ]]; then
  echo "GOOGLE_API_KEY is not set. Gemini will be disabled."
fi


gcloud config set project "$GCP_PROJECT_ID"

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY:-}"
