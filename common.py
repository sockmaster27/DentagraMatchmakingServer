import os


def check_for_confidential_file(path):
    if not os.path.exists(path):
        raise RuntimeError(
            f"{path} does not exist. Please generate new certificate, or request a copy from project owners."
        )
