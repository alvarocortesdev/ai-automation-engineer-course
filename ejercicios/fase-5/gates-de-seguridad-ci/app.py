"""App mínima del ejercicio. No la edites: existe para que el pipeline tenga algo
que lintear y testear. El foco del ejercicio son los YAML de .github/."""


def normaliza_email(email: str) -> str:
    """Normaliza un email: sin espacios y en minúsculas."""
    return email.strip().lower()
