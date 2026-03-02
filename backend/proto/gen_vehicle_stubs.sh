#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

PROTO_FILE="$SCRIPT_DIR/vehicle.proto"

python -m grpc_tools.protoc \
  -I "$SCRIPT_DIR" \
  --python_out "$ROOT_DIR/backend/app" \
  --grpc_python_out "$ROOT_DIR/backend/app" \
  "$PROTO_FILE"

python -m grpc_tools.protoc \
  -I "$SCRIPT_DIR" \
  --python_out "$ROOT_DIR/clients/tkinter" \
  --grpc_python_out "$ROOT_DIR/clients/tkinter" \
  "$PROTO_FILE"

echo "Stubs generados para vehicle.proto"
