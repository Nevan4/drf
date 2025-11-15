# Learning Notes — DRF Mini Project

## Entry — 2025-11-15

- **Topics:** Django trailing-slash behavior, redirects, request body behavior, `model_to_dict` vs DRF Serializer, property fields, client requests

- **Summary:** Built a small DRF endpoint (`api_home`) that returns a random `Product`. Learned why trailing slashes matter, why request bodies are lost on redirects, and why DRF serializers are preferred over `model_to_dict` for API responses.

---


### DRF fundamentals (short)

- **Serializers:** Map model instances to/from JSON. Use `ModelSerializer` for quick mapping; use `SerializerMethodField` to expose `@property` values.
- **Views:** Function-based (`@api_view`) or class-based (`APIView`, `ViewSet`). Prefer `ViewSet` + routers for standard REST resources.
- **Routers & URLs:** Routers auto-generate list/retrieve/create/update/destroy routes for `ViewSet`s.
- **Request / Response:** Use `request.data` for parsed bodies. Return `Response(...)` (DRF) for content negotiation and consistent rendering.
- **Parsers / Renderers:** DRF handles JSON/XML parsing and response rendering (includes browsable API).
- **Auth & Permissions:** Pluggable auth (Token/Session/JWT) and permission classes (`IsAuthenticated`, `IsAdminUser`).
- **Validation & Types:** Serializers support field and object validation and robust type conversion (Decimal, DateTime, etc.).
- **Relationships & Pagination:** Serializers support nested/related representations; DRF provides pagination and filter backends.
- **Testing:** Use `APIClient` for tests (it understands DRF request/response behavior).

---

### DRF: connection diagram (high-level)

Below is a compact diagram showing the typical flow and how the main DRF pieces connect.

```text
                            ┌──────────────────────────┐
                            │  Client (Browser/Mobile) │
                            └──────────────┬───────────┘
                                           │
                               HTTP Request│
                                           v
                            ┌──────────────────────────┐
                            │        WSGI/ASGI         │
                            │ (Django Request Object)  │
                            └──────────────┬───────────┘
                                           v
                            ┌──────────────────────────┐
                            │        URL Router        │
                            │ (URL patterns, path(),   │
                            │  re_path(), routers)     │
                            └──────────────┬───────────┘
                                           v
                            ┌──────────────────────────┐
                            │        View/ViewSet      │
                            │ (dispatch(), as_view(),  │
                            │   action selection)      │
                            └──────────────┬───────────┘
                                           │
                           ┌───────────────┴─────────────────┐
                           │ Authentication & Permissions    │
                           │ (IsAuthenticated, throttling,   │
                           │  custom permissions, auth back.)│
                           └───────────────┬─────────────────┘
                                           v
                            ┌────────────────────────────────┐
                            │        Input Parsing           │
                            │ (JSONParser, FormParser,       │
                            │  MultiPartParser, etc.)        │
                            └────────────────────────────────┘
                                           |
                                           v
                            ┌──────────────────────────┐
                            │      Serializer (in)     │
                            │  .is_valid() -> .data    │
                            │  validation, fields,     │
                            │  nested serializers,     │
                            │  SerializerMethodField   │
                            └──────────────┬───────────┘
                                           │
                                           v
                            ┌──────────────────────────┐
                            │         Model (ORM)      │
                            │  QuerySet operations,    │
                            │  .save(), .create(),     │
                            │  managers, relations     │
                            └──────────────┬───────────┘
                                           │
                                           v
                                        Database
                               (PostgreSQL, SQLite, etc.)
                                           │
                                           v
                            ┌──────────────────────────┐
                            │     Serializer (out)     │
                            │ transforms ORM → JSON    │
                            │ uses fields, methods,    │
                            │ depth, custom logic      │
                            └──────────────┬───────────┘
                                           v
                            ┌──────────────────────────┐
                            │  Renderer (JSONRenderer, │
                            │    BrowsableAPI, etc.)   │
                            └──────────────┬───────────┘
                                           v
                                          Response
                                           │
                                           v
                            ┌──────────────────────────┐
                            │        Client Output     │
                            │   JSON / HTML / YAML     │
                            └──────────────────────────┘

```

Short notes:
- Router maps the incoming URL to a View/ViewSet method (list/retrieve/create/etc.).
- View/ViewSet handles request lifecycle: auth, permission, input (parsers), delegates to serializer for validation and conversion.
- Serializer maps Model <-> native Python types and controls validation and representation (can include `SerializerMethodField` for properties).
- Model is the Django ORM layer that reads/writes the database.
- Parsers / Renderers handle how incoming data is parsed (JSON/form-data) and how responses are rendered (JSON, browsable API).
- Auth and Permissions run before view logic; Response handles status codes and content negotiation.


### SerializerMethodField naming conventions

When you use `SerializerMethodField` in a serializer, DRF automatically looks for a method to call. The **default convention** is `get_<field_name>`:

```python
# Example: field named 'my_discount' → DRF looks for method 'get_my_discount'
my_discount = serializers.SerializerMethodField(read_only=True)

def get_my_discount(self, obj):
    return obj.sale_price
```

**Three approaches to name the method:**

1. **Convention (default):** `get_<field_name>` — DRF auto-discovers it
   ```python
   discount = serializers.SerializerMethodField()  # auto-finds get_discount()
   def get_discount(self, obj): ...
   ```

2. **Custom method name via `method_name` parameter:**
   ```python
   discount = serializers.SerializerMethodField(method_name='compute_discount')
   def compute_discount(self, obj): ...
   ```

3. **Custom method name via `source` parameter:**
   ```python
   discount = serializers.SerializerMethodField(source='calculate_discount')
   def calculate_discount(self, obj): ...
   ```

**Best practice:** Follow the `get_<field_name>` convention — it's predictable and requires no extra configuration.

---

### Key takeaways

- **Trailing slash:** Django endpoints conventionally end with `/`. With `APPEND_SLASH=True`, a request to `/api` returns `301` → `/api/`.
- **Redirects & bodies:** 301/302 redirects typically drop the request body; query parameters are preserved. Avoid redirects when sending body data (use correct URL or POST).
- **Properties:** `model_to_dict` doesn't include `@property` fields (e.g., `sale_price`) — add them manually or use a Serializer.
- **Serializer advantages:** DRF serializers provide validation, type conversion, nested relationships, and can include computed fields (`SerializerMethodField`).
- **@property vs method:** Use `@property` for simple read-only computed values (accessed as `obj.value`); use methods for reusable logic with parameters.

---

### Commands used

```bash
# run the Django server
python manage.py runserver

# test client (remember trailing slash)
python py_client/basic.py
```

---

### Files of interest

| Path | Purpose |
|---|---|
| `backend/api/views.py` | `api_home` view (uses `ProductSerializer`) |
| `backend/products/models.py` | `Product` model with `sale_price` property |
| `backend/products/serializers.py` | place to add `SerializerMethodField` for `sale_price` |
| `py_client/basic.py` | simple script demonstrating client requests |

---


### Next steps (short)


---

## Template for future entries

- **Date:**
- **Topics:**
- **Summary:**
- **Key details:**
- **Commands:**
- **Files:**
- **Next steps / TODO:**
