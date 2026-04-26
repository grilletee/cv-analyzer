import pypdf
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))

    if len(reader.pages) == 0:
        raise ValueError("El PDF está vacío")

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    text = text.strip()

    if not text:
        raise ValueError("No se pudo extraer texto del PDF. Puede ser un PDF escaneado sin OCR")

    return text