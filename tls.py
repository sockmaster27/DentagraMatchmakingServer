import ssl
import os
from typing import Optional


def check_for_confidential_file(path):
    if not os.path.exists(path):
        raise RuntimeError(
            f"{path} does not exist. Please generate new certificate, or request a copy from project owners."
        )


certificate_path = os.path.join("TLS", "matchmaking_cert.pem")
key_path = os.path.join("TLS", "matchmaking_key.key")

check_for_confidential_file(key_path)


def generate_ssl_context(client_cert: Optional[str] = None) -> ssl.SSLContext:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certificate_path, key_path)

    if client_cert:
        ssl_context.load_verify_locations(client_cert)
        ssl_context.verify_mode = ssl.CERT_REQUIRED

    return ssl_context
