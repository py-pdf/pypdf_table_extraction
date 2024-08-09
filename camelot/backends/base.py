class ConversionBackend:

    def installed(self) -> bool:
        raise NotImplementedError

    def convert(self, pdf_path: str, png_path: str, resolution: int = 300) -> None:
        raise NotImplementedError
