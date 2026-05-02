from importlib import import_module

__all__ = [
    "genre_repository",
    "program_repository",
    "report_repository",
    "user_repository",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
