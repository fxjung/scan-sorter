import logging
from typing import Union
from tqdm import tqdm
from pathlib import Path
from rich.progress import track
from pypdf import PdfReader, PdfWriter

log = logging.getLogger(__name__)


def n(i, N):
    if i < N / 2:
        if i % 2:
            return int(N / 2 + i)
        else:
            return int(N / 2 - i)
    else:
        if i % 2:
            return int(i - N / 2)
        else:
            return int(N - (i - N / 2))


def get_ordered_sequence(N: int):
    assert not N % 2, "N must be even"
    return [n(i, N) - 1 for i in range(0, N)]


def reorder_pdf(input_path: Union[str, Path], output_path: Union[str, Path]):
    reader = PdfReader(input_path)
    N = len(reader.pages)
    writer = PdfWriter()

    writer.merge(position=0, fileobj=input_path, pages=get_ordered_sequence(N))
    writer.write(output_path)


def reorder_all_pdfs_in_directory(input_dir: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True, parents=True)
    input_paths = [*input_dir.glob("*.pdf")]
    if not input_paths:
        print("No PDFs in current directory. Done.")
        return
    n_skipped = 0
    # for input_path in track(input_paths, "Processing..."):
    for input_path in tqdm(input_paths):
        output_path = output_dir / input_path.name
        if output_path.exists():
            n_skipped += 1
        else:
            reorder_pdf(input_path=input_path, output_path=output_path)
    print(
        f"{len(input_paths)} files processed, {n_skipped} skipped due to output file existing."
    )
