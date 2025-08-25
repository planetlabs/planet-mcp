import nox

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = False

# Default sessions - all tests, but not packaging
nox.options.sessions = [
    "lint",
    "test",
]

_DEFAULT_PYTHON = "3.13"
_ALL_PYTHON = ["3.11", "3.12", "3.13"]


@nox.session(python=_ALL_PYTHON)
def test(session):
    """Run Pytest test suites"""
    session.run("python", "-m", "ensurepip", "--upgrade")
    session.install("-e", ".[test]")
    session.run("uv", "sync", "--all-groups")
    options = session.posargs
    session.run("uv", "run", "pytest", "-vv", *options)


@nox.session(python=_DEFAULT_PYTHON)
def lint(session):
    """Check code formatting with Black"""
    session.install("-e", ".[dev]")
    session.run(
        "uv", "tool", "run", "black", "--verbose", "--check", "--diff", "--color", "."
    )
    session.run("uv", "tool", "run", "ruff", "--verbose", "check", ".")
