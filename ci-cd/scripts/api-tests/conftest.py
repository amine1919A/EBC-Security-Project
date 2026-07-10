import pytest
import requests

def pytest_configure(config):
    """Configuration pytest pour les tests API EBC"""
    config.addinivalue_line("markers", "security: Marqueur pour tests de sécurité")
    config.addinivalue_line("markers", "owasp_a1: OWASP Top 10 A1 - Injection")
    config.addinivalue_line("markers", "owasp_a2: OWASP Top 10 A2 - Auth")
    config.addinivalue_line("markers", "owasp_a3: OWASP Top 10 A3 - Sensitive Data")
    config.addinivalue_line("markers", "owasp_a5: OWASP Top 10 A5 - Access Control")
    config.addinivalue_line("markers", "owasp_a7: OWASP Top 10 A7 - XSS")
    config.addinivalue_line("markers", "owasp_a9: OWASP Top 10 A9 - Vulnerabilities")
    config.addinivalue_line("markers", "owasp_a10: OWASP Top 10 A10 - Logging")
