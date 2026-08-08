import fitz


def extract_text(pdf_file):

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text()

        pages.append(
            {
                "page": page_number,
                "text": text
            }
        )

    return pages