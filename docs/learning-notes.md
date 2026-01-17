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

## Entry — 2025-11-17

- **Date:** 2025-11-17
- **Topics:** Serializer runtime behavior, validation, instance vs data, save()
- **Summary:** Notes about how DRF serializers behave at runtime: passing `data=` does not create an instance, `is_valid()` and `validated_data` are used for input validation, and `save()` persists to the database and returns an instance which SerializerMethodField methods can work with.
- **Key details:**
   - No DB side-effect without `save()`: using `ProductSerializer(data=request.data)` prepares the serializer for validation only — nothing is written until `serializer.save()` is called.
   - Instance-dependent fields: `SerializerMethodField` is called with an object instance when serializing model instances. When using the serializer for input (`data=`) there is no `obj`; guard with `hasattr(obj, 'id')` or `isinstance(obj, Product)` in `get_<field>` methods.
   - Validation diagnostics: use `serializer.is_valid(raise_exception=True)` to get informative errors (wrong type, missing required fields) that explain why save/serialization cannot proceed.
   - Where to compute values: compute derived values from `serializer.validated_data` before calling `save()`, or call `serializer.save()` then serialize the returned instance for response values that depend on model methods/properties.
   - `validated_data` vs `data`: after `is_valid()`, use `serializer.validated_data` for cleaned input; `serializer.data` is the serialized representation (output) and requires either validated input or an instance.
- **Commands:**
   - Use `is_valid(raise_exception=True)` in views to get immediate feedback.

- **Files:**
   - `backend/api/views.py` — example view using `ProductSerializer(data=request.data)`
   - `backend/products/serializers.py` — SerializerMethodField examples and guards

- **Next steps / TODO:**
   - Add a short example view flow in the notes: `is_valid() -> save() -> ProductSerializer(instance).data`

---

## Entry — 2025-11-29

- **Date:** 2025-11-29
- **Topics:** DRF generics (RetrieveAPIView), app-level URL layout, wiring class-based views, minimal view config
- **Summary:** Added a Product detail view using DRF's RetrieveAPIView and noted how to expose it via an app-level urls.py and wire it into the project URLconf.

- **Key details:**
  - RetrieveAPIView is the simplest generic view for single-object GETs: it implements get_object() and standard response behavior so you don't have to write boilerplate.
  - Keep URL patterns next to the app: add `products/urls.py` inside the products app and put product endpoints there to keep routing organized by feature.
  - In the project URLconf include the app urls and map class-based views with `.as_view()`. Example patterns:
    - By pk: `path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail')`
    - By slug: `path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail')` plus `lookup_field = 'slug'` on the view.
  - ProductDetailAPIView minimal setup: set `queryset = Product.objects.all()` and `serializer_class = ProductSerializer`. These provide the object lookup and the serialization logic; add `lookup_field` or permission classes as needed.

- **Commands:**
  - run server: `python manage.py runserver`
  - quick client check: `python py_client/detail.py` (expects `http://localhost:8000/api/products/1/`)

- **Files of interest:**
  - `backend/products/views.py` — ProductDetailAPIView (queryset, serializer_class, optional lookup_field)
  - `backend/products/urls.py` — app-level routes for products (create if missing)
  - `backend/urls.py` (project URLconf) — include app URLs with `include('products.urls')`
  - `py_client/detail.py` — simple requests-based test client

- **Next steps / TODO:**
  - Add `products/urls.py` if not present and register it in the project URLconf.
  - Consider adding tests that exercise both pk and slug lookups if slug support is added.

---

## Entry — 2025-12-02

- **Date:** 2025-12-02
- **Topics:** DRF generics (CreateAPIView), app-level URL routing, perform_create override, POST request handling
- **Summary:** Added ProductCreateAPIView using DRF's CreateAPIView to handle POST requests and persist new products to the database. Wired create and detail endpoints in app-level urls.py and demonstrated client-side POST with create.py script.

- **Key details:**
  - CreateAPIView is the simplest generic view for single-object POSTs: it implements post() dispatch, serializer validation, and save() logic so you don't have to write boilerplate.
  - Override perform_create() to customize save behavior: this hook receives the validated serializer and allows you to set additional fields (e.g., `serializer.save(content=content)`) before persisting to the database.
  - App-level URL routing: define create and detail routes in `products/urls.py` using `.as_view()`. Typical patterns:
    - Create (POST/GET form): `path('', ProductCreateAPIView.as_view(), name='product-create')`
    - Detail (GET by pk): `path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail')`
  - ProductCreateAPIView minimal setup: set `queryset = Product.objects.all()` and `serializer_class = ProductSerializer`. Override `perform_create()` if you need to compute or inject fields (e.g., default content from title, set user, etc.).
  - Client-side POST: use requests library with `json=` parameter to send JSON body; the server parses and validates with the serializer.

- **Commands:**
  - run server: `python manage.py runserver`
  - test create endpoint: `python py_client/create.py` (sends POST to `http://localhost:8000/api/products/`)
  - test detail endpoint: `python py_client/detail.py` (sends GET to `http://localhost:8000/api/products/1/`)

- **Files of interest:**
  - `backend/products/views.py` — ProductCreateAPIView (perform_create override example), ProductDetailAPIView
  - `backend/products/urls.py` — app-level routes (create '', detail '<int:pk>/')
  - `backend/urls.py` (project URLconf) — include app URLs with `include('products.urls')`
  - `py_client/create.py` — POST request to create new product
  - `py_client/detail.py` — GET request to retrieve product by id

- **Next steps / TODO:**

---

## Template for future entries

- **Date:**
- **Topics:**
- **Summary:**
- **Key details:**
- **Commands:**
- **Files:**

## Entry — 2025-01-13 (Branch 1-11)

- **Date:** 2025-01-13
- **Topics:** DRF generics (ListAPIView, ListCreateAPIView), app-level URL consolidation, unified routing
- **Summary:** Replaced individual ProductDetailAPIView and ProductCreateAPIView with a unified ProductListCreateAPIView to handle both GET (list) and POST (create) on a single endpoint. Updated URL routing to consolidate create and list operations.

- **Key details:**
  - ListCreateAPIView combines list (GET /) and create (POST /) into a single view class: implements both `list()` and `create()` actions with minimal configuration.
  - Single endpoint pattern: instead of separate views, one `ProductListCreateAPIView` handles both operations on `path('', ...)`, reducing boilerplate and improving cohesion.
  - App-level URLs now simpler: `path('', ProductListCreateAPIView.as_view())` for list/create, `path('<int:pk>/', ProductDetailAPIView.as_view())` for detail.
  - Override `perform_create()` as before to customize create behavior (e.g., set default content from title).
  - Client scripts updated: `list.py` for GET (retrieve all products), `create.py` for POST (add new product), `detail.py` for GET by pk.

- **Commands:**
  - run server: `python manage.py runserver`
  - test list endpoint: `python py_client/list.py` (sends GET to `http://localhost:8000/api/products/`)
  - test create endpoint: `python py_client/create.py` (sends POST to `http://localhost:8000/api/products/`)
  - test detail endpoint: `python py_client/detail.py` (sends GET to `http://localhost:8000/api/products/1/`)

- **Files of interest:**
  - `backend/products/views.py` — ProductListCreateAPIView (combined list/create)
  - `backend/products/urls.py` — consolidated routing
  - `py_client/list.py`, `py_client/create.py`, `py_client/detail.py` — client test scripts

- **Next steps / TODO:**
  - Consider using UpdateAPIView and DestroyAPIView for full CRUD (PATCH, DELETE).
  - Explore filtering, searching, and pagination for the list endpoint.

---

## Entry — 2025-01-13 (Branch 1-12)

- **Date:** 2025-01-13
- **Topics:** Function-based views with @api_view decorator, unified GET/POST handling, type checking with cast()
- **Summary:** Replaced DRF generic class-based views (ListCreateAPIView, RetrieveAPIView) with a single function-based view (`product_alt_view`) using the `@api_view` decorator. Demonstrated how to handle both GET (list/detail) and POST (create) in one function based on request method and URL parameters, while managing type-checker issues with explicit `cast()`.

- **Key details:**
  - `@api_view(['GET', 'POST'])` decorator turns a function into a DRF view that accepts specified HTTP methods.
  - Single function, unified logic: check `request.method` and `pk` parameter to route list (GET /), detail (GET /<pk>/), and create (POST /) operations.
  - GET detail: `if pk is not None:` fetch object with `get_object_or_404(Product, pk=pk)`, serialize and return.
  - GET list: `if pk is None:` fetch all products with `Product.objects.all()`, serialize with `many=True` and return.
  - POST create: validate with `serializer.is_valid(raise_exception=True)`, extract validated data with `cast(dict, serializer.validated_data)` to satisfy type checker, compute fields (e.g., default content from title), save and return with status 201.
  - Type checker workaround: use `cast(dict, serializer.validated_data)` to explicitly tell the type checker that validated_data is a dict; prevents spurious "empty" attribute errors when using `.get()`.
  - URL routing: `path('')` for list/create, `path('<int:pk>/')` for detail — Django's URLconf passes `pk` to the view function.

- **Commands:**
  - run server: `python manage.py runserver`
  - test list/create: `python py_client/list.py` (GET), `python py_client/create.py` (POST)
  - test detail: `python py_client/detail.py` (GET by pk)

- **Files of interest:**
  - `backend/products/views.py` — `product_alt_view` function-based view with `@api_view` decorator
  - `backend/products/urls.py` — routes mapped to `product_alt_view`
  - `py_client/` — client test scripts (list, create, detail)

- **Pros of function-based views:**
  - More explicit control flow (easier to read for simple cases).
  - Direct access to request.method and URL parameters.

- **Cons:**
  - Less DRY: logic branches per HTTP method; harder to extend with permissions/throttling.
  - More manual error handling.
  - Less opinionated about REST patterns.

- **Comparison:** Generic class-based views (like ListCreateAPIView) provide structure and reusability; function-based views offer simplicity for one-off endpoints or non-standard patterns.

---

## Entry — 2026-01-17

- **Date:** 2026-01-17
- **Topics:** Refactoring to generic class-based views, complete CRUD operations, URL routing consolidation
- **Summary:** Refactored the products app to use DRF generic class-based views exclusively. Replaced the function-based `product_alt_view` with dedicated generic views for all CRUD operations: `ProductListCreateAPIView`, `ProductDetailAPIView`, `ProductUpdateAPIView`, and `ProductDestroyAPIView`. Updated URL routing to reflect the new endpoint structure with proper separation of concerns.

- **Key details:**
  - Replaced function-based `product_alt_view` with specialized generic views for better separation of concerns and DRY principles.
  - `ProductListCreateAPIView` (extends `ListCreateAPIView`): Handles GET (list all) and POST (create new) on the list endpoint.
  - `ProductDetailAPIView` (extends `RetrieveAPIView`): Handles GET (retrieve single) by pk.
  - `ProductUpdateAPIView` (extends `UpdateAPIView`): Handles PUT (full update) with custom `perform_update` to ensure content field defaults to title if empty.
  - `ProductDestroyAPIView` (extends `DestroyAPIView`): Handles DELETE requests.
  - New URL patterns: `/api/products/`, `/api/products/<pk>/`, `/api/products/<pk>/update/`, `/api/products/<pk>/delete/`.

- **Commands:**
  - run server: `python manage.py runserver`
  - client tests: `python py_client/list.py`, `python py_client/detail.py`, `python py_client/create.py`, `python py_client/update.py`, `python py_client/delete.py`

- **Files modified:**
  - `backend/products/views.py` — Added 4 generic views, commented out `product_alt_view`
  - `backend/products/urls.py` — Updated URL patterns to route to the new generic views
  - `py_client/update.py` (new) — Test script for PUT requests
  - `py_client/delete.py` (new) — Test script for DELETE requests

---

## Entry — 2026-01-17 (Mixins exploration)

- **Date:** 2026-01-17
- **Topics:** DRF mixins, combining mixins with GenericAPIView, understanding view lifecycle and validation
- **Summary:** Explored DRF mixins by building `ProductMixinView` that combines `CreateModelMixin`, `ListModelMixin`, `RetrieveModelMixin`, and `GenericAPIView`. Learned how mixins handle the full HTTP lifecycle—including automatic `is_valid()` calls—allowing a single view to handle both list (`/products/`) and detail (`/products/<pk>/`) operations with GET and POST methods.

- **Key details:**
  - **Mixins:** Reusable building blocks that implement specific behaviors (`CreateModelMixin`, `ListModelMixin`, `RetrieveModelMixin`). Each mixin provides methods like `create()`, `list()`, `retrieve()` that handle the full request lifecycle.
  - **GenericAPIView base:** Provides common view setup (queryset, serializer_class, lookup_field) that mixins rely on.
  - **Automatic validation:** When `self.create()` is called, the mixin automatically calls `is_valid()` internally before invoking `perform_create()`. This means `validated_data` is guaranteed to be available in `perform_create()` without explicit validation.
  - **Method dispatch:** The view's `get()` and `post()` methods manually dispatch to `self.retrieve()`, `self.list()`, or `self.create()` based on URL parameters (pk presence).
  - **Single view, multiple operations:** One view class handles both `/products/` (list/create) and `/products/<pk>/` (retrieve) by checking if pk exists in kwargs.

- **Commands:**
  - Test with client: `python py_client/create.py`, `python py_client/list.py`, etc.

- **Files modified:**
  - `backend/products/views.py` — Added `ProductMixinView` using mixins; previous generic views still present
  - `backend/products/urls.py` — Switched routes to use `ProductMixinView` instead of specific generic views
  - `py_client/create.py` — Updated test data

- **Key learning:**
  - Mixins abstract away boilerplate: they handle `is_valid()`, error handling, response formatting automatically
  - `perform_create()` is called by the mixin after validation passes—you don't need to validate manually
  - Mixins demonstrate the hidden workflow: `get()` → mixin method → validation (automatic) → `perform_*()` → DB operation → Response

