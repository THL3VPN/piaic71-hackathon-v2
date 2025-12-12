# Contract: GET /health

- **Method/Path**: `GET /health`
- **Auth**: None
- **Request Body**: None
- **Response**:
  - **Status**: 200 OK
  - **Body**: JSON object

```json
{
  "status": "ok"
}
```

- **Errors**: None expected; endpoint should respond even without upstream dependencies.
