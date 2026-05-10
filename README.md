# FastAPI middleware in this project

This project now shows the two FastAPI patterns that most closely match Express middleware:

1. Global middleware in `main.py`
2. Router-level guard with `Depends(...)`

## 1. Global middleware

In Express, you would normally write:

```js
app.use((req, res, next) => {
	console.log(req.method, req.url);
	next();
});
```

In this FastAPI project, the equivalent lives in `main.py`:

```python
@app.middleware("http")
async def log_and_time_requests(request: Request, call_next):
		started_at = time.perf_counter()
		print(f"{request.method} {request.url.path}")

		response = await call_next(request)

		duration = time.perf_counter() - started_at
		response.headers["X-Process-Time"] = f"{duration:.6f}"
		return response
```

This runs for every request, logs the request, and adds an `X-Process-Time` response header.

## 2. Router-level auth guard

In Express, you would often do this:

```js
router.use(authMiddleware);
```

In this FastAPI project, the equivalent is a dependency attached to the router:

```python
router = APIRouter(
		prefix="/users",
		tags=["Users"],
		dependencies=[Depends(verify_authorization_header)],
)
```

The actual check lives in `dependencies/auth.py` and expects this header:

```http
Authorization: Bearer demo-token
```

## 3. How to test it

Start the app:

```bash
uv run uvicorn main:app --reload
```

Open docs:

```text
http://127.0.0.1:8000/docs
```

Test the public root route:

```bash
curl -i http://127.0.0.1:8000/
```

Test a protected users route without a token:

```bash
curl -i http://127.0.0.1:8000/users/
```

Test the same route with the demo token:

```bash
curl -i \
	-H "Authorization: Bearer demo-token" \
	http://127.0.0.1:8000/users/
```

## 4. Express to FastAPI mapping

- `app.use(middleware)` -> `@app.middleware("http")`
- `router.use(auth)` -> `dependencies=[Depends(auth_dependency)]`
- `req.someValue = ...` -> `request.state.some_value = ...`
- `next()` -> `await call_next(request)`
