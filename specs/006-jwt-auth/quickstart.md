# Quickstart: JWT-protected API

1. **Set the shared secret** – create `.env` entries:
   ```env
   BETTER_AUTH_SECRET=super-secret-token
   ```
2. **Run backend with UV**:
   ```bash
   export BETTER_AUTH_SECRET=super-secret-token
   uv run uvicorn src.main:app --reload --port 8000
   ```
3. **Use the sample test token** (expires in 2030) when calling protected endpoints:
   ```bash
   export BETTER_AUTH_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZW1vLXVzZXIiLCJleHAiOjE4OTM0MzgwMDB9.8qSAo6l5S8MjcHpuugCbe6cfn2x020yVNJnXEumhCmo
   curl -H "Authorization: Bearer $BETTER_AUTH_TOKEN" http://localhost:8000/api/tasks
   ```
4. **Run pytest** to exercise auth paths:
   ```bash
   BETTER_AUTH_SECRET=replace-with-shared-secret uv run python3.13 -m pytest tests/unit/test_auth_middleware.py
   ```
5. **Run coverage command** to prove auth suite stays green alongside the full backend tests:
   ```bash
   BETTER_AUTH_SECRET=replace-with-shared-secret uv run python3.13 -m pytest --cov=src
   ```
