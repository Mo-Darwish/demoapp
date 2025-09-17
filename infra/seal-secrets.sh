#!/bin/bash

# Script to seal raw-secrets.yaml into watchtower-sealed-secret.yaml
# Usage: ./seal-secrets.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Files
RAW_FILE="raw-secrets.yaml"
SEALED_FILE="demoapp-sealed-secret.yaml"

echo -e "${GREEN}Sealing Secrets${NC}"
echo "================"

# Check if raw secrets file exists
if [ ! -f "$RAW_FILE" ]; then
  echo -e "${RED}Error: $RAW_FILE not found${NC}"
  echo "Please create $RAW_FILE with your secret values first"
  exit 1
fi

# Check if kubeseal is installed
if ! command -v kubeseal &>/dev/null; then
  echo -e "${RED}Error: kubeseal is not installed${NC}"
  echo "Install with: brew install kubeseal"
  exit 1
fi

# Check if sealed secrets controller is installed
echo -e "${YELLOW}Checking for Sealed Secrets controller...${NC}"

# Try common controller names and namespaces
CONTROLLER_NAME=""
CONTROLLER_NAMESPACE=""

# Check common locations
for ns in "kube-system" "sealed-secrets" "default"; do
  for name in "sealed-secrets-controller" "sealed-secrets"; do
    if kubectl get service "$name" -n "$ns" &>/dev/null; then
      CONTROLLER_NAME="$name"
      CONTROLLER_NAMESPACE="$ns"
      echo -e "${GREEN}✓ Found controller: $name in namespace: $ns${NC}"
      break 2
    fi
  done
done

if [ -z "$CONTROLLER_NAME" ]; then
  echo -e "${RED}✗ Sealed Secrets controller not found${NC}"
  echo ""
  echo "To install Sealed Secrets controller:"
  echo "  helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets"
  echo "  helm repo update"
  echo "  helm install sealed-secrets -n kube-system sealed-secrets/sealed-secrets"
  echo ""
  echo "Or if it's installed with a custom name, update this script with:"
  echo "  --controller-name <name> --controller-namespace <namespace>"
  exit 1
fi

# Seal the secrets
echo -e "${YELLOW}Sealing $RAW_FILE -> $SEALED_FILE${NC}"
echo -e "${YELLOW}Note: This will completely replace the existing secret, not merge with it${NC}"

# Use --scope strict to ensure the secret can only be decrypted in the specified namespace
# The sealed secret will completely replace any existing secret when applied
if kubeseal --controller-name "$CONTROLLER_NAME" --controller-namespace "$CONTROLLER_NAMESPACE" --scope strict --format=yaml <"$RAW_FILE" >"$SEALED_FILE"; then
  echo -e "${GREEN}✓ Successfully created $SEALED_FILE${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Review the sealed secret: cat $SEALED_FILE"
  echo "2. Apply to cluster (this will REPLACE the entire secret): kubectl apply -f $SEALED_FILE"
  echo "3. Commit the sealed secret: git add $SEALED_FILE && git commit -m 'Update sealed secrets'"
  echo ""
  echo -e "${YELLOW}Important: The sealed secret will completely replace the existing secret in the cluster.${NC}"
  echo -e "${YELLOW}Any keys not in $RAW_FILE will be removed from the cluster secret.${NC}"
  echo -e "${YELLOW}Remember: Never commit $RAW_FILE!${NC}"
else
  echo -e "${RED}✗ Failed to seal secrets${NC}"
  echo "Make sure:"
  echo "1. kubectl is configured with cluster access"
  echo "2. Sealed Secrets controller is installed in the cluster"
  exit 1
fi
