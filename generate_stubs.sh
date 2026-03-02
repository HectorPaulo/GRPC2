#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python -m grpc_tools.protoc \
  -I "$ROOT_DIR/backend/proto" \
  --python_out "$ROOT_DIR/backend/app" \
  --grpc_python_out "$ROOT_DIR/backend/app" \
  "$ROOT_DIR/backend/proto/vehicle.proto"

python -m grpc_tools.protoc \
  -I "$ROOT_DIR/backend/proto" \
  --python_out "$ROOT_DIR/clients/tkinter" \
  --grpc_python_out "$ROOT_DIR/clients/tkinter" \
  "$ROOT_DIR/backend/proto/vehicle.proto"

echo "Stubs Python generados."
