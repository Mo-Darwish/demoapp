#!/bin/bash

# Script to extract a sealed secret back to raw-secrets.yaml
# This requires cluster access and proper permissions
# Usage: ./extract-sealed-secrets.sh [sealed-secret-file]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
NAMESPACE="default"
SECRET_NAME="demoapp"
OUTPUT_FILE="raw-secrets.yaml"

echo -e "${GREEN}Extract Sealed Secrets${NC}"
echo "======================"

# Function to extract from cluster
extract_from_cluster() {
  echo -e "${YELLOW}Extracting secret '$SECRET_NAME' from namespace '$NAMESPACE'...${NC}"

  if kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" &>/dev/null; then
    # Get the secret and convert data to stringData with decoded values
    cat >"$OUTPUT_FILE" <<'EOF'
# DO NOT COMMIT THIS FILE - IT CONTAINS PLAIN TEXT SECRETS
# Edit this file with your actual secret values, then run ./seal-secrets.sh

apiVersion: v1
kind: Secret
metadata:
  name: demoapp
  namespace: default
type: Opaque
stringData:
EOF

    # Extract and decode each secret
    kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o json |
      jq -r '.data | to_entries[] | "  \(.key): \"\(.value | @base64d)\""' >>"$OUTPUT_FILE"

    echo -e "${GREEN}✓ Secret extracted and decoded to $OUTPUT_FILE${NC}"
    echo -e "${YELLOW}WARNING: $OUTPUT_FILE contains plain text secrets!${NC}"
    echo "Remember to:"
    echo "1. Edit the secrets as needed"
    echo "2. Run ./seal-secrets.sh to create new sealed secret"
    echo "3. NEVER commit $OUTPUT_FILE"
  else
    echo -e "${RED}Error: Secret '$SECRET_NAME' not found in namespace '$NAMESPACE'${NC}"
    exit 1
  fi
}

# Function to create template if no secret exists
create_template() {
  echo -e "${YELLOW}Creating template file...${NC}"

  cat >"$OUTPUT_FILE" <<'EOF'
# DO NOT COMMIT THIS FILE - IT CONTAINS PLAIN TEXT SECRETS
# Edit this file with your actual secret values, then run ./seal-secrets.sh

apiVersion: v1
kind: Secret
metadata:
  name: demoapp
  namespace: default
type: Opaque
stringData:
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    SECRET_KEY = 'django-insecure-gm!p+(jzf$k_%$2+es3lf8)(bcy#04xx4&t85!a7a(*1ytbz0&'
    DATABASE_URL= postgresql://postgres.cjgpqhzschsrpbpetwrz:FFsXUOl2ujU2DcdE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
    # CELERY_BROKER_URL= redis://default:AGNSstCcK06Nm4pW4RuBz6tIjPzXOxT3@redis-14289.c74.us-east-1-4.ec2.redns.redis-cloud.com:14289
    # CELERY_RESULT_BACKEND= redis://default:AGNSstCcK06Nm4pW4RuBz6tIjPzXOxT3@redis-14289.c74.us-east-1-4.ec2.redns.redis-cloud.com:14289
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
EOF

  echo -e "${GREEN}✓ Template created at $OUTPUT_FILE${NC}"
  echo "Fill in your secret values and run ./seal-secrets.sh"
}

# Main logic
if [ "$1" = "--template" ]; then
  create_template
else
  # Check kubectl access
  if ! kubectl cluster-info &>/dev/null; then
    echo -e "${RED}Error: kubectl not configured or cluster not accessible${NC}"
    echo "To create a template instead, run: $0 --template"
    exit 1
  fi

  extract_from_cluster
fi
