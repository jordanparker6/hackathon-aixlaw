import argparse
from pathlib import Path
from la


def ingest(file: Path):

    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        url=url,
        prefer_grpc=True,
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="my_documents",
    )


def main(args):
    _dir = Path(args.input)

    files = list(_dir.glob("**/*.pdf"))

    for file in files:
        ingest(file)

s

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()
