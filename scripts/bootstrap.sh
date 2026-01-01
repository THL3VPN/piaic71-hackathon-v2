#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT}/.env"
FRONTEND_ENV="${ROOT}/frontend/.env.local"

usage() {
  cat <<'EOF'
Usage: ./scripts/bootstrap.sh [env|backend|frontend|mcp]

Commands
  env       Sync frontend/.env.local from .env
  backend   Load .env, sync frontend env, and run uvicorn (FastAPI) on BACKEND_PORT
  frontend  Sync env and run Next.js dev server on FRONTEND_PORT
  mcp       Load .env and run MCP server on MCP_PORT

Prereq: create .env (e.g., cp .env.example .env) and fill secrets/tokens.
EOF
}

ensure_env() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing .env at repo root. Copy .env.example and fill in values." >&2
    exit 1
  fi
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
  : "${BETTER_AUTH_SECRET:?BETTER_AUTH_SECRET must be set in .env}"
  : "${DATABASE_URL:?DATABASE_URL must be set in .env (Postgres/Neon)}"
  export UV_PYTHON="${UV_PYTHON:-python3.13}"
  export UV_CACHE_DIR="${UV_CACHE_DIR:-${ROOT}/.uv-cache}"
  export BACKEND_PORT="${BACKEND_PORT:-8000}"
  export FRONTEND_PORT="${FRONTEND_PORT:-3000}"
  export MCP_SERVER_URL="${MCP_SERVER_URL:-http://localhost:9000}"
  export NEXT_PUBLIC_BACKEND_URL="${NEXT_PUBLIC_BACKEND_URL:-http://localhost:${BACKEND_PORT}}"
}

sync_frontend_env() {
  ensure_env
  mkdir -p "${ROOT}/frontend"
  cat > "${FRONTEND_ENV}" <<EOF
NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}
EOF
  echo "Wrote ${FRONTEND_ENV}"
}

run_backend() {
  ensure_env
  sync_frontend_env
  if [[ ! -d "${ROOT}/.venv" ]]; then
    (cd "${ROOT}" && uv sync)
  fi
  cd "${ROOT}"
  exec uv run uvicorn src.main:app --reload --port "${BACKEND_PORT}"
}

run_frontend() {
  ensure_env
  sync_frontend_env
  cd "${ROOT}/frontend"
  if [[ ! -d node_modules ]]; then
    npm install
  fi
  exec npm run dev -- --hostname 0.0.0.0 --port "${FRONTEND_PORT}"
}

run_mcp() {
  ensure_env
  if [[ ! -d "${ROOT}/.venv" ]]; then
    (cd "${ROOT}" && uv sync)
  fi
  cd "${ROOT}"
  export PYTHONPATH="${ROOT}"
  exec uv run python mcp_server/app.py
}

cmd="${1:-}"
case "${cmd}" in
  env) sync_frontend_env ;;
  backend) run_backend ;;
  frontend) run_frontend ;;
  mcp) run_mcp ;;
  *) usage; exit 1 ;;
esac
