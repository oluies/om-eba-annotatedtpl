#!/bin/sh
# Do the three roles auto-ontology needs actually answer on the on-premise endpoint?
# Usage: ONPREM_BASE=http://<host>:8000/v1 [EMBED_MODEL=...] [RERANK_MODEL=...] sh probe_onprem.sh
: "${ONPREM_BASE:?set ONPREM_BASE to the OpenAI-compatible base URL}"
KEY="${ONPREM_KEY:-none}"
CHAT="${CHAT_MODEL:-nvidia/nemotron-3.5-super-vl-120b-a12b}"

say() { printf '\n== %s\n' "$1"; }

say "1. models the endpoint lists"
curl -s -H "Authorization: Bearer $KEY" "$ONPREM_BASE/models" |
  python3 -c 'import json,sys; d=json.load(sys.stdin); print("\n".join(m["id"] for m in d.get("data",[])))' 2>/dev/null ||
  echo "  (could not parse /models)"

say "2. chat with structured output - the capability the ingestion needs"
curl -s -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  "$ONPREM_BASE/chat/completions" -d '{
    "model": "'"$CHAT"'",
    "messages": [{"role": "user", "content": "Name the business term for a column called Y0101_r0190_c0020."}],
    "max_tokens": 120,
    "response_format": {"type": "json_schema", "json_schema": {"name": "term", "strict": true,
      "schema": {"type": "object", "additionalProperties": false,
                 "properties": {"term": {"type": "string"}, "confidence": {"type": "number"}},
                 "required": ["term", "confidence"]}}}
  }' | head -c 600

say "3. embeddings"
if [ -n "$EMBED_MODEL" ]; then
  curl -s -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
    "$ONPREM_BASE/embeddings" \
    -d '{"model": "'"$EMBED_MODEL"'", "input": ["Trusted beneficiary (Art.13 RTS)"], "input_type": "passage"}' |
    python3 -c 'import json,sys; d=json.load(sys.stdin); v=d["data"][0]["embedding"]; print("dimensions:", len(v))' 2>/dev/null ||
    echo "  no embedding served here"
else
  echo "  skipped: set EMBED_MODEL"
fi

say "4. ranking (optional - auto-ontology falls back if it fails)"
if [ -n "$RERANK_MODEL" ]; then
  curl -s -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
    "$ONPREM_BASE/ranking" \
    -d '{"model": "'"$RERANK_MODEL"'", "query": {"text": "fraudulent credit transfers"},
         "passages": [{"text": "Trusted beneficiary"}, {"text": "Low value payments"}], "truncate": "END"}' | head -c 300
else
  echo "  skipped: set RERANK_MODEL"
fi
printf '\n'
