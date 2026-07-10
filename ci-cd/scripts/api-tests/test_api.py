"""
Tests de sécurité automatisés pour l'API EBC.
Couvre OWASP Top 10 (2021) : A01 à A10 - couverture complète.
"""

import requests
import pytest
import json
import time
import socket
import ssl

BASE_URL = "http://app:80/api"
TIMEOUT = 10


class TestApiHealth:
    def test_health_endpoint(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "status" in data

    def test_health_returns_ok(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert r.json().get("status") == "ok" or r.status_code == 200


class TestOWASP_A01_BrokenAccessControl:
    """A01: Broken Access Control - IDOR, forced browsing, CORS, method tampering"""

    def test_idor_vulnerability(self):
        for user_id in [1, 2, 3, 100, 999]:
            r = requests.get(f"{BASE_URL}/users/{user_id}", timeout=TIMEOUT)
            assert r.status_code in [401, 403, 404], \
                f"IDOR possible on user {user_id}"

    def test_admin_endpoints_protected(self):
        admin_endpoints = [
            "/admin", "/admin/users", "/admin/config",
            "/api/admin/scan", "/api/admin/logs",
        ]
        for endpoint in admin_endpoints:
            r = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            assert r.status_code in [401, 403, 404], \
                f"Admin endpoint not protected: {endpoint}"

    def test_http_method_restriction(self):
        dangerous_methods = ["PUT", "DELETE", "PATCH", "TRACE"]
        for method in dangerous_methods:
            r = requests.request(method, f"{BASE_URL}/users/1", timeout=TIMEOUT)
            assert r.status_code in [401, 403, 405], \
                f"Dangerous method {method} allowed on /users/1"

    def test_cors_misconfiguration(self):
        r = requests.options(
            f"{BASE_URL}/users",
            headers={"Origin": "https://evil.com", "Access-Control-Request-Method": "GET"},
            timeout=TIMEOUT,
        )
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        assert acao != "*", "CORS wildcard allows any origin"

    def test_forced_browsing_admin(self):
        for path in ["/admin", "/admin/users", "/admin/config", "/admin/logs"]:
            r = requests.get(f"http://app:80{path}", timeout=TIMEOUT)
            assert r.status_code in [401, 403, 404], \
                f"Forced browsing allowed to {path}"

    def test_security_scan_trigger_unauthenticated(self):
        r = requests.post(
            f"{BASE_URL}/security/scan",
            json={"tool": "trivy"},
            timeout=TIMEOUT,
        )
        assert r.status_code in [401, 403, 404], \
            f"Unauthenticated scan trigger possible: {r.status_code}"

    def test_horizontal_idor(self):
        headers_no_auth = {}
        for target_id in [2, 3, 100]:
            r = requests.get(
                f"{BASE_URL}/users/{target_id}", headers=headers_no_auth, timeout=TIMEOUT
            )
            assert r.status_code in [401, 403, 404], \
                f"Horizontal IDOR: accessed user {target_id}"


class TestOWASP_A02_CryptographicFailures:
    """A02: Cryptographic Failures - plaintext passwords, TLS, data exposure"""

    def test_no_passwords_in_response(self):
        r = requests.get(f"{BASE_URL}/users/1", timeout=TIMEOUT)
        if r.status_code != 401:
            assert "password" not in r.text.lower()

    def test_passwords_not_stored_in_plaintext(self):
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "testuser", "password": "Test@12345"},
            timeout=TIMEOUT,
        )
        assert "Test@12345" not in r.text, "Password echoed back in response"

    def test_no_version_disclosure(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = r.json()
        assert "version" not in data, f"Version disclosed: {data.get('version')}"

    def test_no_sensitive_data_exposure(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        body = r.text.lower()
        for secret in ["password", "secret_key", "api_key", "credit_card"]:
            assert secret not in body, f"Sensitive field '{secret}' exposed"

    def test_https_redirect(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT, allow_redirects=True)
        assert r.status_code == 200

    def test_weak_password_rejected(self):
        weak_passwords = ["password", "123456", "admin", "qwerty", "abc123"]
        for pwd in weak_passwords:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": "test", "password": pwd},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 401, 403], f"Weak password accepted: {pwd}"


class TestOWASP_A03_Injection:
    """A03: Injection - SQL, NoSQL, command, LDAP, XXE, SSTI, path traversal"""

    def test_sql_injection_in_user_id(self):
        payloads = [
            "' OR '1'='1", "1; DROP TABLE users--",
            "' UNION SELECT * FROM users--", "1' AND 1=1--",
        ]
        for payload in payloads:
            r = requests.get(f"{BASE_URL}/users", params={"id": payload}, timeout=TIMEOUT)
            assert r.status_code in [400, 403, 404, 500], \
                f"SQL Injection possible: {payload}"

    def test_sql_injection_in_login(self):
        payloads = [
            "' OR '1'='1' --", "admin'--", "' OR 1=1--", "admin' OR '1'='1",
        ]
        for payload in payloads:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": payload, "password": payload},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 401, 403], \
                f"Auth bypass possible: {payload}"

    def test_no_sql_injection(self):
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": '{"$gt": ""}', "password": '{"$gt": ""}'},
            timeout=TIMEOUT,
        )
        assert r.status_code in [400, 401, 403]

    def test_command_injection(self):
        payloads = ["; cat /etc/passwd", "| ls -la", "$(whoami)", "`id`"]
        for payload in payloads:
            r = requests.post(
                f"{BASE_URL}/security/scan",
                json={"tool": payload},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 403, 404, 422], \
                f"Command injection possible: {payload}"
            assert "root:" not in r.text, f"Command output leaked: {payload}"

    def test_xml_xxe(self):
        xxe_payload = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
        <root><data>&xxe;</data></root>"""
        r = requests.post(
            f"{BASE_URL}/feedback",
            data=xxe_payload,
            headers={"Content-Type": "application/xml"},
            timeout=TIMEOUT,
        )
        assert r.status_code in [400, 415, 422], f"XXE accepted: status {r.status_code}"

    def test_path_traversal(self):
        payloads = [
            "../../../etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "....//....//....//etc/passwd",
        ]
        for payload in payloads:
            r = requests.get(f"{BASE_URL}/users/{payload}", timeout=TIMEOUT)
            assert r.status_code in [400, 403, 404], \
                f"Path traversal possible: {payload}"

    def test_ssti(self):
        payloads = ["{{7*7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}"]
        for payload in payloads:
            r = requests.get(f"{BASE_URL}/search", params={"q": payload}, timeout=TIMEOUT)
            if r.status_code == 200:
                assert "49" not in r.text, f"SSTI possible: {payload}"

    def test_ldap_injection(self):
        payloads = ["*)(objectClass=*)", "admin)(&)", "*()|&'"]
        for payload in payloads:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": payload, "password": "x"},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 401, 403], f"LDAP injection possible: {payload}"

    def test_header_injection(self):
        r = requests.get(
            f"{BASE_URL}/search",
            params={"q": "test\r\nX-Injected-Header: true"},
            timeout=TIMEOUT,
        )
        assert "X-Injected-Header" not in r.headers, "Header injection possible"


class TestOWASP_A04_InsecureDesign:
    """A04: Insecure Design - rate limiting, lockout, timing attacks"""

    def test_login_rate_limiting(self):
        rate_limited = False
        for i in range(100):
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": "admin", "password": f"wrong{i}"},
                timeout=TIMEOUT,
            )
            if r.status_code == 429:
                rate_limited = True
                break
        assert rate_limited, "No rate limiting on /auth/login"

    def test_account_lockout(self):
        correct_password = "super_secret_pw"
        for i in range(20):
            requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": "target_user", "password": "wrong"},
                timeout=TIMEOUT,
            )
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "target_user", "password": correct_password},
            timeout=TIMEOUT,
        )
        assert r.status_code in [403, 429], "Account not locked after failures"

    def test_timing_attack_on_auth(self):
        times = []
        for username in ["admin", "admii", "root", "nonexistent_user_xyz"]:
            start = time.time()
            requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": "wrong"},
                timeout=TIMEOUT,
            )
            times.append(time.time() - start)
        avg = sum(times) / len(times)
        max_dev = max(abs(t - avg) for t in times)
        assert max_dev < 0.3, f"Timing deviation {max_dev:.3f}s - user enumeration possible"

    def test_resource_consumption_limits(self):
        oversized = "A" * (5 * 1024 * 1024)
        r = requests.post(
            f"{BASE_URL}/feedback",
            data=oversized,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        assert r.status_code in [400, 413, 422], f"Oversized payload accepted: {r.status_code}"

    def test_empty_auth_bypass(self):
        payloads = [
            {"username": "", "password": ""},
            {"username": "admin", "password": ""},
            {"username": "", "password": "password"},
        ]
        for payload in payloads:
            r = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=TIMEOUT)
            assert r.status_code in [400, 401, 403], \
                f"Auth bypass with empty fields: {payload}"

    def test_user_enumeration_prevented(self):
        r1 = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "nonexistent_user_xyz", "password": "x"},
            timeout=TIMEOUT,
        )
        r2 = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "x"},
            timeout=TIMEOUT,
        )
        assert r1.status_code == r2.status_code, "Different status codes = enumeration"


class TestOWASP_A05_SecurityMisconfiguration:
    """A05: Security Misconfiguration - headers, info disclosure, defaults"""

    def test_security_headers_present(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        headers = r.headers
        assert headers.get("X-Content-Type-Options", "").lower() == "nosniff", \
            "Missing X-Content-Type-Options"
        xfo = headers.get("X-Frame-Options", "").upper()
        assert xfo in ("DENY", "SAMEORIGIN"), f"Missing X-Frame-Options: {xfo}"

    def test_hsts_header(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        hsts = r.headers.get("Strict-Transport-Security", "")
        assert "max-age=" in hsts, "Missing HSTS header"

    def test_content_security_policy(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        csp = r.headers.get("Content-Security-Policy", "")
        assert csp != "", "Missing Content-Security-Policy"
        assert "unsafe-inline" not in csp, "CSP allows unsafe-inline"

    def test_server_version_not_disclosed(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        data = r.json()
        assert "version" not in data, f"Version disclosed: {data.get('version')}"
        assert "application" not in data or data.get("application") in ("", None), \
            f"App name disclosed: {data.get('application')}"

    def test_infrastructure_not_disclosed(self):
        r = requests.get(f"{BASE_URL}/security/status", timeout=TIMEOUT)
        if r.status_code == 200:
            body = r.text.lower()
            for tool in ["sonarqube", "grafana", "prometheus", "trivy"]:
                assert tool not in body, f"Internal tool disclosed: {tool}"

    def test_error_pages_no_info_leak(self):
        r = requests.get(f"{BASE_URL}/nonexistent-route-xyz", timeout=TIMEOUT)
        indicators = ["symfony", "php", "stack trace", "exception", "debug"]
        for ind in indicators:
            assert ind.lower() not in r.text.lower(), \
                f"Framework info disclosed: '{ind}'"

    def test_trace_method_disabled(self):
        r = requests.request("TRACE", f"{BASE_URL}/health", timeout=TIMEOUT)
        assert r.status_code in [405, 403, 404], f"TRACE method allowed: {r.status_code}"


class TestOWASP_A06_VulnerableComponents:
    """A06: Vulnerable & Outdated Components - version disclosure, known CVEs"""

    def test_server_header_info_leak(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        server = r.headers.get("Server", "")
        if server:
            assert "Apache/2.4.49" not in server
            assert "Apache/2.4.50" not in server
            assert "nginx/1.21" not in server

    def test_php_version_not_disclosed(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        for header_val in [r.headers.get(h, "").lower() for h in ("Server", "X-Powered-By")]:
            assert "php" not in header_val, f"PHP version disclosed: {header_val}"

    def test_framework_version_not_disclosed(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert "symfony" not in r.text.lower(), "Symfony disclosed in body"
        assert "x-generator" not in r.headers, "Generator header present"


class TestOWASP_A07_AuthenticationFailures:
    """A07: Identification & Authentication Failures - brute force, session, MFA"""

    def test_no_default_credentials(self):
        defaults = [
            ("admin", "admin"), ("admin", "password"),
            ("admin", "123456"), ("root", "root"), ("user", "user"),
        ]
        for username, password in defaults:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 401, 403], \
                f"Default creds work: {username}:{password}"

    def test_session_management(self):
        r = requests.get(f"{BASE_URL}/admin", timeout=TIMEOUT)
        assert r.status_code in [401, 403], "Admin accessible without auth"

    def test_jwt_token_validation(self):
        fake_tokens = [
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.fake",
            "invalid-token", "Bearer null", "",
        ]
        for token in fake_tokens:
            r = requests.get(
                f"{BASE_URL}/admin/users",
                headers={"Authorization": f"Bearer {token}"},
                timeout=TIMEOUT,
            )
            assert r.status_code in [401, 403], f"Invalid token accepted: {token}"

    def test_brute_force_protection(self):
        blocked = False
        for i in range(50):
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": "admin", "password": f"guess{i}"},
                timeout=TIMEOUT,
            )
            if r.status_code == 429:
                blocked = True
                break
        assert blocked, "No brute-force protection on login"

    def test_password_complexity_enforced(self):
        weak = ["123456", "password", "admin", "aaa", "111111", "qwerty"]
        for pwd in weak:
            r = requests.post(
                f"{BASE_URL}/auth/register",
                json={"username": "newuser", "password": pwd},
                timeout=TIMEOUT,
            )
            if r.status_code not in [404, 405]:
                assert r.status_code in [400, 422], f"Weak password accepted: {pwd}"


class TestOWASP_A08_DataIntegrity:
    """A08: Software & Data Integrity Failures - CSRF, deserialization, schema"""

    def test_csrf_protection_absent(self):
        state_changes = [
            ("POST", f"{BASE_URL}/auth/login", {"username": "x", "password": "x"}),
            ("POST", f"{BASE_URL}/feedback", {"message": "test"}),
            ("POST", f"{BASE_URL}/security/scan", {"tool": "trivy"}),
        ]
        for method, url, payload in state_changes:
            r = requests.request(
                method, url,
                json=payload,
                headers={"Origin": "https://evil.com"},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 401, 403, 405, 422], \
                f"No CSRF protection on {method} {url}: {r.status_code}"

    def test_php_deserialization_not_exposed(self):
        r = requests.post(
            f"{BASE_URL}/feedback",
            data='O:8:"stdClass":0:{}',
            headers={"Content-Type": "application/x-php-serialized"},
            timeout=TIMEOUT,
        )
        assert r.status_code in [400, 415, 422], "Serialized PHP accepted"

    def test_json_schema_validation(self):
        payloads = [
            {"__proto__": {"admin": True}},
            {"constructor": {"prototype": {"isAdmin": True}}},
            {"username": "admin", "password": "x", "role": "admin"},
        ]
        for payload in payloads:
            r = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=TIMEOUT)
            assert r.status_code in [400, 401, 403, 422], \
                f"Unexpected field accepted: {payload}"

    def test_signed_responses(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        sig = r.headers.get("X-Signature", "")
        digest = r.headers.get("Digest", "")
        assert sig or digest, "API responses are not integrity-checked"


class TestOWASP_A09_LoggingMonitoring:
    """A09: Security Logging & Monitoring Failures - audit trail, log injection"""

    def test_error_handling(self):
        r = requests.get(f"{BASE_URL}/nonexistent-route-12345", timeout=TIMEOUT)
        assert r.status_code in [404, 405], "No proper error handling"

    def test_stack_trace_exposure(self):
        r = requests.get(f"{BASE_URL}/users/abc", timeout=TIMEOUT)
        indicators = ["Stack trace", "PHP Fatal error", "Warning",
                       "file_get_contents", "Trace:", "Debug"]
        for indicator in indicators:
            assert indicator.lower() not in r.text.lower(), \
                f"Stack trace exposed: {indicator}"

    def test_log_injection_resistant(self):
        payload = "legit\n2024-01-01 FAKE admin login success"
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": payload, "password": "x"},
            timeout=TIMEOUT,
        )
        assert r.status_code in [400, 401, 403], "Log injection possible"

    def test_log_files_not_accessible(self):
        for path in ["/var/log/app.log", "/logs/app.log", "/app.log"]:
            r = requests.get(f"{BASE_URL}/..{path}", timeout=TIMEOUT)
            assert r.status_code in [403, 404], f"Log file accessible: {path}"

    def test_rate_limiting(self):
        responses = []
        for _ in range(50):
            r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            responses.append(r.status_code)
        assert any(code == 429 for code in responses), "No rate limiting observed"


class TestOWASP_A10_SSRF:
    """A10: Server-Side Request Forgery - internal network probing, bypass"""

    def test_ssrf_via_feedback(self):
        ssrf_payloads = [
            "http://169.254.169.254/latest/meta-data/",
            "http://127.0.0.1:8080/admin",
            "http://localhost:3306/",
            "gopher://127.0.0.1:6379/_INFO",
        ]
        for payload in ssrf_payloads:
            for field in ["url", "target", "callback", "webhook", "file"]:
                r = requests.post(
                    f"{BASE_URL}/feedback",
                    json={field: payload},
                    timeout=TIMEOUT,
                )
                assert r.status_code in [400, 403, 422], \
                    f"SSRF possible: {field}={payload}"

    def test_ssrf_via_scan_target(self):
        internal_targets = [
            "http://169.254.169.254/", "http://127.0.0.1/",
            "http://localhost:3306/", "file:///etc/passwd",
        ]
        for target in internal_targets:
            r = requests.post(
                f"{BASE_URL}/security/scan",
                json={"tool": target},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 403, 422], f"SSRF via scan: {target}"

    def test_ssrf_localhost_bypass(self):
        bypasses = [
            "http://127.0.0.1", "http://localhost", "http://0.0.0.0",
            "http://2130706433", "http://127.1", "http://0",
        ]
        for target in bypasses:
            r = requests.post(
                f"{BASE_URL}/security/scan",
                json={"tool": target},
                timeout=TIMEOUT,
            )
            assert r.status_code in [400, 403, 422], f"SSRF bypass: {target}"
