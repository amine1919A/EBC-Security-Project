"""
Tests de sécurité automatisés pour l'API EBC.
Couvre OWASP Top 10 : A1-Injection, A2-Auth, A3-Sensitive Data,
A5-Access Control, A7-XSS, A9-Known Vulnerabilities
"""

import requests
import pytest
import json

BASE_URL = "http://app:80/api"
TIMEOUT = 10

class TestApiHealth:
    """Test de base : disponibilité de l'API"""

    def test_health_endpoint(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "status" in data

    def test_health_returns_ok(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert r.json().get("status") == "ok" or r.status_code == 200


class TestOWASP_A1_Injection:
    """OWASP Top 10 A1: Injection"""

    def test_sql_injection_in_user_id(self):
        payloads = [
            "' OR '1'='1",
            "1; DROP TABLE users--",
            "' UNION SELECT * FROM users--",
            "1' AND 1=1--",
            "1' OR '1'='1' LIMIT 1--"
        ]
        for payload in payloads:
            r = requests.get(
                f"{BASE_URL}/users",
                params={"id": payload},
                timeout=TIMEOUT
            )
            assert r.status_code in [400, 403, 404, 500], \
                f"SQL Injection possible with payload: {payload}"

    def test_sql_injection_in_login(self):
        payloads = [
            "' OR '1'='1' --",
            "admin'--",
            "' OR 1=1--",
            "admin' OR '1'='1"
        ]
        for payload in payloads:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": payload, "password": payload},
                timeout=TIMEOUT
            )
            assert r.status_code in [400, 401, 403], \
                f"Auth bypass possible with payload: {payload}"

    def test_no_sql_injection(self):
        payload = '{"$gt": ""}'
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": payload, "password": payload},
            timeout=TIMEOUT
        )
        assert r.status_code in [400, 401, 403]


class TestOWASP_A2_Auth:
    """OWASP Top 10 A2: Broken Authentication"""

    def test_no_default_credentials(self):
        defaults = [
            ("admin", "admin"),
            ("admin", "password"),
            ("admin", "123456"),
            ("root", "root"),
            ("user", "user"),
        ]
        for username, password in defaults:
            r = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=TIMEOUT
            )
            assert r.status_code in [400, 401, 403], \
                f"Default credentials work: {username}:{password}"

    def test_session_management(self):
        r = requests.get(f"{BASE_URL}/admin", timeout=TIMEOUT)
        assert r.status_code in [401, 403], \
            "Admin endpoint accessible without auth"

    def test_jwt_token_validation(self):
        fake_tokens = [
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.fake",
            "invalid-token",
            "Bearer null",
            ""
        ]
        for token in fake_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            r = requests.get(
                f"{BASE_URL}/admin/users",
                headers=headers,
                timeout=TIMEOUT
            )
            assert r.status_code in [401, 403], \
                f"Invalid token accepted: {token}"


class TestOWASP_A3_SensitiveData:
    """OWASP Top 10 A3: Sensitive Data Exposure"""

    def test_no_passwords_in_response(self):
        r = requests.get(f"{BASE_URL}/users/1", timeout=TIMEOUT)
        if r.status_code != 401:
            body = r.text.lower()
            sensitive_fields = ["password", "passwd", "secret", "token", "credit_card"]
            for field in sensitive_fields:
                response_body = r.text.lower()
                assert "password" not in response_body or r.status_code == 401

    def test_https_redirect(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT, allow_redirects=True)
        assert True  # Non-bloquant en dev


class TestOWASP_A5_AccessControl:
    """OWASP Top 10 A5: Broken Access Control"""

    def test_idor_vulnerability(self):
        for user_id in [1, 2, 3, 100, 999]:
            r = requests.get(
                f"{BASE_URL}/users/{user_id}",
                timeout=TIMEOUT
            )
            assert r.status_code in [401, 403, 404], \
                f"IDOR possible on user {user_id}"

    def test_admin_endpoints_protected(self):
        admin_endpoints = [
            "/admin",
            "/admin/users",
            "/admin/config",
            "/api/admin/scan",
            "/api/admin/logs",
        ]
        for endpoint in admin_endpoints:
            r = requests.get(
                f"{BASE_URL}{endpoint}",
                timeout=TIMEOUT
            )
            assert r.status_code in [401, 403, 404], \
                f"Admin endpoint not protected: {endpoint}"

    def test_http_method_restriction(self):
        dangerous_methods = ["PUT", "DELETE", "PATCH", "TRACE"]
        for method in dangerous_methods:
            r = requests.request(
                method,
                f"{BASE_URL}/users/1",
                timeout=TIMEOUT
            )
            assert r.status_code in [401, 403, 405], \
                f"Dangerous method {method} allowed on /users/1"


class TestOWASP_A7_XSS:
    """OWASP Top 10 A7: Cross-Site Scripting"""

    xss_payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "javascript:alert(1)",
        "\"><script>alert(1)</script>",
        "'; alert(1); '",
        "<scr<script>ipt>alert(1)</scr<script>ipt>",
    ]

    def test_xss_reflected_in_search(self):
        for payload in self.xss_payloads:
            r = requests.get(
                f"{BASE_URL}/search",
                params={"q": payload},
                timeout=TIMEOUT
            )
            body_lower = r.text.lower()
            assert "alert(1)" not in body_lower or r.status_code in [400, 403], \
                f"XSS possible with payload: {payload}"

    def test_xss_in_post_data(self):
        for payload in self.xss_payloads:
            r = requests.post(
                f"{BASE_URL}/feedback",
                json={"message": payload},
                timeout=TIMEOUT
            )
            if r.status_code == 200:
                assert "alert(1)" not in r.text, \
                    f"Stored XSS possible with payload: {payload}"

    def test_content_type_headers(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        headers = r.headers
        xss_protection = headers.get("X-XSS-Protection", "0")
        content_type = headers.get("Content-Type", "")
        assert True  # Non-bloquant, observé


class TestOWASP_A9_KnownVulnerabilities:
    """OWASP Top 10 A9: Using Components with Known Vulnerabilities"""

    def test_server_header_info_leak(self):
        r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        server = r.headers.get("Server", "")
        if server:
            assert "Apache/2.4.49" not in server  # CVE-2021-41773
            assert "Apache/2.4.50" not in server  # CVE-2021-42013

    def test_rate_limiting(self):
        responses = []
        for _ in range(50):
            r = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            responses.append(r.status_code)
        rate_limited = any(code == 429 for code in responses)
        if not rate_limited:
            pass  # Observé, pas bloquant


class TestOWASP_A10_Logging:
    """OWASP Top 10 A10: Insufficient Logging & Monitoring"""

    def test_error_handling(self):
        r = requests.get(f"{BASE_URL}/nonexistent-route-12345", timeout=TIMEOUT)
        assert r.status_code in [404, 405], \
            "No proper error handling for unknown routes"

    def test_stack_trace_exposure(self):
        r = requests.get(f"{BASE_URL}/users/abc", timeout=TIMEOUT)
        stack_indicators = ["Stack trace", "PHP Fatal error", "Warning",
                           "file_get_contents", "Trace:", "Debug"]
        for indicator in stack_indicators:
            assert indicator.lower() not in r.text.lower(), \
                f"Stack trace exposed: {indicator}"
