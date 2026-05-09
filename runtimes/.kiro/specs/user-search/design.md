# Design: User Search

## Architecture

```text
Search UI -> GET /api/users/search -> validator -> tenant scope -> indexed query -> response
```

The feature adds one endpoint to the existing users service and one UI surface in the existing admin application. It does not add a new service or datastore.

## API

`GET /api/users/search`

Query parameters:

- `q`: optional case-insensitive substring for name/email.
- `role`: optional exact role.
- `status`: optional exact status.
- `created_after`, `created_before`: optional ISO dates.
- `cursor`: optional opaque pagination cursor.
- `limit`: optional page size, capped at 50.

Response:

```json
{
  "items": [
    {
      "id": "usr_123",
      "name": "Example User",
      "email": "user@example.com",
      "role": "admin",
      "status": "active"
    }
  ],
  "next_cursor": "opaque-cursor",
  "total_estimate": 42
}
```

## Data

Add indexes for lowercased name, lowercased email, role, and status. No table columns change.

## Failure Modes

- Invalid query parameters return `400` with field-level errors.
- Unauthorized callers return `401`.
- Callers without user-directory permission return `403`.
- Backend failures return `500` with a request ID and no query-string echo.

## Observability

Emit metrics for latency, result count, validation errors, authorization failures, and cache hit rate if a cache is added.
