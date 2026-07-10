import pytest

def pytest_configure(config):
    """Configuration pytest pour les tests API EBC - OWASP Top 10 2021"""
    config.addinivalue_line("markers", "security: Marqueur pour tests de sécurité")
    config.addinivalue_line("markers", "owasp_a01: OWASP Top 10 A01 - Broken Access Control")
    config.addinivalue_line("markers", "owasp_a02: OWASP Top 10 A02 - Cryptographic Failures")
    config.addinivalue_line("markers", "owasp_a03: OWASP Top 10 A03 - Injection")
    config.addinivalue_line("markers", "owasp_a04: OWASP Top 10 A04 - Insecure Design")
    config.addinivalue_line("markers", "owasp_a05: OWASP Top 10 A05 - Security Misconfiguration")
    config.addinivalue_line("markers", "owasp_a06: OWASP Top 10 A06 - Vulnerable & Outdated Components")
    config.addinivalue_line("markers", "owasp_a07: OWASP Top 10 A07 - Authentication Failures")
    config.addinivalue_line("markers", "owasp_a08: OWASP Top 10 A08 - Data Integrity Failures")
    config.addinivalue_line("markers", "owasp_a09: OWASP Top 10 A09 - Logging & Monitoring Failures")
    config.addinivalue_line("markers", "owasp_a10: OWASP Top 10 A10 - SSRF")
