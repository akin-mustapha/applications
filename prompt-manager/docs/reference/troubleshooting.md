---
name: Troubleshooting
---

# Troubleshooting

Common setup and runtime issues with Prompt Manager and how to fix them.

---

## MongoDB

### MongoDB won't start

**Symptom:** `docker-compose up -d` fails or the container exits immediately.

**Checks:**

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs mongo
```

**Common causes:**

- Docker Desktop is not running — start it first
- Port 27017 is already in use (see port conflicts below)
- Insufficient disk space for Docker volumes

---

### FastAPI can't connect to MongoDB

**Symptom:** API returns `500 Internal Server Error` on any request. Logs show a connection error to MongoDB.

**Checks:**

1. Confirm MongoDB is running: `docker-compose ps`
2. Confirm `MONGO_URI` in `.env` is correct:

   ```env
   MONGO_URI=mongodb://localhost:27017
   ```

3. Confirm `.env` is being loaded — check that `python-dotenv` is installed and `config.py` calls `load_dotenv()`

4. Test the connection directly:

   ```bash
   docker exec -it <mongo-container-name> mongosh
   ```

---

### UUID index not created on startup

**Symptom:** Slow queries or duplicate UUID errors after multiple creates.

**Fix:** The FastAPI app should create a unique index on `id` for both collections at startup:

```python
collection.create_index("id", unique=True)
```

Confirm this is present in `src/main.py` startup logic. If the index is missing, add it and restart the service.

---

## Port Conflicts

### Port 27017 already in use

**Symptom:** `docker-compose up` fails with "port is already allocated".

**Fix:**

```bash
# Find what's using the port
lsof -i :27017

# Kill the process if it's a stale MongoDB instance
kill -9 <PID>

# Or change the host port in docker-compose.yml
ports:
  - "27018:27017"  # use 27018 on the host instead
```

If you change the host port, update `MONGO_URI` in `.env` to match:

```env
MONGO_URI=mongodb://localhost:27018
```

---

### Port 8000 already in use

**Symptom:** `uvicorn src.main:app --reload` fails with "address already in use".

**Fix:**

```bash
# Find what's using the port
lsof -i :8000

# Kill it, or run uvicorn on a different port
uvicorn src.main:app --reload --port 8001
```

If you change the port, update `API_BASE_URL` in `.env`:

```env
API_BASE_URL=http://localhost:8001
```

---

### Port 8050 already in use

**Symptom:** `python src/app.py` fails or another Dash app is running.

**Fix:**

```bash
lsof -i :8050
kill -9 <PID>
```

Or configure Dash to use a different port in `src/app.py`:

```python
app.run(port=8051)
```

---

## Environment Variables

### `.env` file missing

**Symptom:** App starts but `MONGO_URI` or `API_BASE_URL` is `None`. Crashes or connection failures follow.

**Fix:**

```bash
cp .env.example .env
```

Then open `.env` and set the values. See [dev-setup.md](../engineering/dev-setup.md) for the correct defaults.

---

### `.env` not loaded

**Symptom:** Env vars exist in `.env` but the app doesn't see them.

**Checks:**

- `python-dotenv` is installed: `pip show python-dotenv`
- `src/config.py` calls `load_dotenv()` before reading vars
- The working directory when running the app is the project root (where `.env` lives)

---

## Python / Virtual Environment

### `uvicorn` module not found

**Symptom:** `python: No module named uvicorn` or `uvicorn: command not found`.

**Fix:** Your virtual environment is not active, or dependencies weren't installed:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

### `ruff` not found

**Symptom:** `ruff: command not found`.

**Fix:**

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
```

---

### `pytest` not found

**Symptom:** `pytest: command not found`.

**Fix:**

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
```

---

## Dash Frontend

### Dash UI shows blank page

**Symptom:** `http://localhost:8050` loads but no content appears, or the sidebar is empty.

**Most likely cause:** The Dash frontend can't reach the FastAPI service.

**Checks:**

1. Is the FastAPI service running? Visit `http://localhost:8000/docs` — if that 404s, the service is down.
2. Is `API_BASE_URL` in `.env` set correctly?

   ```env
   API_BASE_URL=http://localhost:8000
   ```

3. Check the browser developer console (F12) for failed HTTP requests.

---

### Dash callbacks show error toast

**Symptom:** A visible error appears in the UI after an action.

The Dash frontend reads `response["detail"]` from FastAPI error responses. Open the browser console to see the raw error, then check the FastAPI logs for the root cause.

---

## Tests

### Integration tests fail to connect to MongoDB

**Symptom:** `pytest tests/integration/` hangs or errors with a connection refused message.

**Fix:** MongoDB must be running before integration tests:

```bash
docker-compose up -d
pytest tests/integration/
```

---

### Tests leave data in the database

**Symptom:** Test results vary depending on run order, or previous test data appears in later tests.

**Fix:** Ensure `conftest.py` has an `autouse=True` fixture that clears the test collections before (or after) each test. See [testing.md](../engineering/testing.md) for the fixture pattern.
