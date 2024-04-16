import ctypes
import sys
from ctypes.util import find_library

from camelot.backends.base import ConversionBackend


def installed_posix() -> bool:
    library = find_library("gs")
    return library is not None


def installed_windows() -> bool:
    library = find_library(
        "".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll"))  # type: ignore[attr-defined]
    )
    return library is not None


class GhostscriptBackend(ConversionBackend):
    def installed(self) -> bool:
        if sys.platform in ["linux", "darwin"]:
            return installed_posix()
        elif sys.platform == "win32":
            return installed_windows()
        else:
            return installed_posix()

    def convert(self, pdf_path: str, png_path: str, resolution: int = 300) -> None:
        if not self.installed():
            raise OSError(
                "Ghostscript is not installed. You can install it using the instructions"
                " here: https://camelot-py.readthedocs.io/en/master/user/install-deps.html"
            )

        import ghostscript  # type: ignore[import-untyped]

        gs_command = [
            "gs",
            "-q",
            "-sDEVICE=png16m",
            "-o",
            png_path,
            f"-r{resolution}",
            pdf_path,
        ]
        ghostscript.Ghostscript(*gs_command)
