from planet import Session, __version__

_session: Session | None = None


def _init_session(cls: type[Session]) -> Session:
    _session = cls()
    # todo add our version?
    _session._client.headers["User-Agent"] = f"planet-mcp {__version__}"
    return _session


def session() -> Session:
    """session returns a global Session. dependencies should only call this
    in their tool/resource calls or within a callable `mcp` initializer
    """
    global _session
    if _session is None:
        _session = _init_session(Session)
    return _session
