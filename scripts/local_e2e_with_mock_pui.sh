#!/usr/bin/env bash

set -euo pipefail

ADAPTER_BASE_URL="${ADAPTER_BASE_URL:-http://localhost:8000}"
PUI_MOCK_BASE_URL="${PUI_MOCK_BASE_URL:-http://localhost:8010}"
PAYLOAD_TEMPLATE="${PAYLOAD_TEMPLATE:-scripts/payloads/activar_reporte.json}"
TMP_DIR="$(mktemp -d)"
PAYLOAD_FILE="$TMP_DIR/activar_reporte.json"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

REPORT_ID="${REPORT_ID:-$(python3 - <<'PY'
import uuid
print(f"LOCALPUI-{uuid.uuid4()}")
PY
)}"

python3 - <<PY
from pathlib import Path
template = Path("$PAYLOAD_TEMPLATE").read_text(encoding="utf-8")
Path("$PAYLOAD_FILE").write_text(template.replace("__REPORT_ID__", "$REPORT_ID"), encoding="utf-8")
PY

echo "1. Adapter health"
curl --fail --silent --show-error "$ADAPTER_BASE_URL/health" | python3 -m json.tool

echo
echo "2. Mock PUI health"
curl --fail --silent --show-error "$PUI_MOCK_BASE_URL/health" | python3 -m json.tool

echo
echo "3. Dispatch activar-reporte desde PUI mock"
curl --fail --silent --show-error \
  -X POST "$PUI_MOCK_BASE_URL/dispatch/activar-reporte" \
  -H "Content-Type: application/json" \
  --data "@$PAYLOAD_FILE" | python3 -m json.tool

echo
echo "4. Estado acumulado en PUI mock"
curl --fail --silent --show-error "$PUI_MOCK_BASE_URL/state" | python3 -m json.tool

echo
echo "E2E local completado"
echo "REPORT_ID=$REPORT_ID"
