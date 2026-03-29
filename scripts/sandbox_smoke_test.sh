#!/usr/bin/env bash

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
PUI_INBOUND_USER="${PUI_INBOUND_USER:-PUI}"
PUI_INBOUND_PASSWORD="${PUI_INBOUND_PASSWORD:-}"
PAYLOAD_TEMPLATE="${PAYLOAD_TEMPLATE:-scripts/payloads/activar_reporte_prueba.json}"
TMP_DIR="$(mktemp -d)"
LOGIN_RESPONSE_FILE="$TMP_DIR/login.json"
PAYLOAD_FILE="$TMP_DIR/activar_reporte_prueba.json"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

if [[ -z "$PUI_INBOUND_PASSWORD" ]]; then
  echo "PUI_INBOUND_PASSWORD es obligatorio" >&2
  exit 1
fi

if [[ ! -f "$PAYLOAD_TEMPLATE" ]]; then
  echo "No existe PAYLOAD_TEMPLATE: $PAYLOAD_TEMPLATE" >&2
  exit 1
fi

REPORT_ID="${REPORT_ID:-$(python3 - <<'PY'
import uuid
print(f"TESTPUI-{uuid.uuid4()}")
PY
)}"

python3 - <<PY
from pathlib import Path
template = Path("$PAYLOAD_TEMPLATE").read_text(encoding="utf-8")
Path("$PAYLOAD_FILE").write_text(template.replace("__REPORT_ID__", "$REPORT_ID"), encoding="utf-8")
PY

echo "1. Healthcheck"
curl --fail --silent --show-error "$BASE_URL/health" | python3 -m json.tool

echo
echo "2. Login"
curl --fail --silent --show-error \
  -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"usuario\":\"$PUI_INBOUND_USER\",\"clave\":\"$PUI_INBOUND_PASSWORD\"}" \
  > "$LOGIN_RESPONSE_FILE"

python3 -m json.tool "$LOGIN_RESPONSE_FILE"

TOKEN="$(python3 - <<PY
import json
from pathlib import Path
print(json.loads(Path("$LOGIN_RESPONSE_FILE").read_text(encoding="utf-8"))["token"])
PY
)"

echo
echo "3. activar-reporte-prueba"
curl --fail --silent --show-error \
  -X POST "$BASE_URL/activar-reporte-prueba" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  --data "@$PAYLOAD_FILE" | python3 -m json.tool

echo
echo "Smoke test completado"
echo "REPORT_ID=$REPORT_ID"
