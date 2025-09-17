from pathlib import Path
import nox
import shutil

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = False
BUILD_DIRS = ["build", "dist"]

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


@nox.session
def watch(session):
    """Build and serve live docs for editing"""
    session.install("-e", ".[docs]")

    session.run("mkdocs", "serve")


@nox.session
def examples(session):
    session.install("-e", ".[test]")

    options = session.posargs

    # Because these example scripts can be long-running, output the
    # example's stdout so we know what's happening
    session.run("pytest", "--no-cov", "examples/", "-s", *options)


@nox.session
def build(session):
    """Build package"""
    # check preexisting
    exist_but_should_not = [p for p in BUILD_DIRS if Path(p).is_dir()]
    if exist_but_should_not:
        session.error(
            f"Pre-existing {', '.join(exist_but_should_not)}. "
            "Run clean session and try again"
        )

    session.install("build", "twine", "check-wheel-contents")

    session.run(*"python -m build --sdist --wheel".split())
    session.run("check-wheel-contents", "dist")


@nox.session
def clean(session):
    """Remove build directories"""
    to_remove = [Path(d) for d in BUILD_DIRS if Path(d).is_dir()]
    for p in to_remove:
        shutil.rmtree(p)


@nox.session
def publish_testpypi(session):
    """Publish to TestPyPi using API token"""
    _publish(session, "testpypi")


@nox.session
def publish_pypi(session):
    """Publish to PyPi using API token"""
    _publish(session, "pypi")


def _publish(session, repository):
    missing = [p for p in BUILD_DIRS if not Path(p).is_dir()]
    if missing:
        session.error(
            f"Missing one or more build directories: {', '.join(missing)}. "
            "Run build session and try again"
        )

    session.install("twine")

    files = [str(f) for f in Path("dist").iterdir()]
    session.run("twine", "check", *files)
    session.run("twine", "upload", f"--repository={repository}", "-u=__token__", *files)
