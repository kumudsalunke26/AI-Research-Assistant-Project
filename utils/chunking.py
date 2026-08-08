from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []

    for page in pages:

        page_number = page["page"]

        page_text = page["text"]

        split_chunks = splitter.split_text(page_text)

        for chunk in split_chunks:

            chunks.append(
                {
                    "text": chunk,
                    "page": page_number
                }
            )

    return chunks