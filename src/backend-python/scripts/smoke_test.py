"""Live API smoke tests against running backend on port 3001."""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:3001"
results = []


def test(name, method, path, data=None, headers=None, expect_status=200):
    url = BASE + path
    hdrs = headers or {}
    try:
        if data:
            body = json.dumps(data).encode()
            hdrs["Content-Type"] = "application/json"
        else:
            body = None
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        resp = urllib.request.urlopen(req)
        status = resp.status
        resp_data = json.loads(resp.read().decode())
        ok = status == expect_status
        results.append((name, "PASS" if ok else "FAIL", status, resp_data))
        return resp_data
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            resp_data = json.loads(e.read().decode())
        except Exception:
            resp_data = {}
        ok = status == expect_status
        results.append((name, "PASS" if ok else "FAIL", status, resp_data))
        return resp_data
    except Exception as ex:
        results.append((name, "ERROR", 0, str(ex)))
        return {}


# 1. Health
test("Health check", "GET", "/api/health")

# 2. Login
login_resp = test(
    "Login with test user",
    "POST",
    "/api/auth/login",
    {"email": "test@example.com", "password": "Test1234!"},
)
token = login_resp.get("token", "")
auth = {"Authorization": f"Bearer {token}"}

# 3. Me
test("Get current user (/me)", "GET", "/api/auth/me", headers=auth)

# 4. Hosts
test("List hosts", "GET", "/api/hosts")

# 5. Categories (auth required)
cat_resp = test("List categories", "GET", "/api/dictionary/categories", headers=auth)

# 6. Category words
if cat_resp and isinstance(cat_resp, list) and len(cat_resp) > 0:
    cat_id = cat_resp[0].get("id", "")
    test(
        f"Category words ({cat_id[:8]}...)",
        "GET",
        f"/api/dictionary/categories/{cat_id}/words",
        headers=auth,
    )

# 7. Search
test("Search for word (hello)", "GET", "/api/search?q=hello", headers=auth)

# 8. Profile
test("Get profile", "GET", "/api/profile", headers=auth)

# 9. Progress
test("Get progress", "GET", "/api/progress", headers=auth)

# 10. Unauthenticated access (should fail)
test(
    "Categories without auth (expect 401)",
    "GET",
    "/api/dictionary/categories",
    expect_status=401,
)

# 11. Wrong password (expect 401)
test(
    "Login wrong password (expect 401)",
    "POST",
    "/api/auth/login",
    {"email": "test@example.com", "password": "wrong"},
    expect_status=401,
)

# 12. Frontend check
try:
    req = urllib.request.Request("http://localhost:5176/", method="GET")
    resp = urllib.request.urlopen(req)
    html = resp.read().decode()
    has_root = "id=" in html or "<div" in html
    results.append(
        ("Frontend serves HTML", "PASS" if has_root else "FAIL", resp.status, f"{len(html)} bytes")
    )
except Exception as ex:
    results.append(("Frontend serves HTML", "ERROR", 0, str(ex)))


# Print results
print()
print("=" * 65)
print("  SMOKE TEST RESULTS")
print("=" * 65)
passed = sum(1 for r in results if r[1] == "PASS")
failed = sum(1 for r in results if r[1] != "PASS")
for name, status, code, data in results:
    icon = "PASS" if status == "PASS" else "FAIL"
    summary = ""
    if isinstance(data, dict):
        summary = str(data)[:70]
    elif isinstance(data, list):
        summary = f"[{len(data)} items]"
    else:
        summary = str(data)[:70]
    print(f"  [{icon}] {name}")
    print(f"         HTTP {code} -> {summary}")
print()
print(f"  Total: {len(results)} | Passed: {passed} | Failed: {failed}")
print("=" * 65)

sys.exit(0 if failed == 0 else 1)
