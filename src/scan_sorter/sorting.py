import logging

import operator as op

from typing import Union
from setuptools.dist import sequence
from tqdm import tqdm
from pathlib import Path
from rich.progress import track
from pypdf import PdfReader, PdfWriter

log = logging.getLogger(__name__)


def n(i, N) -> int:
    """
    Return the true (expected) page number of the page at position i in the input PDF.

    The assumption being that the input PDF contains a scanned booklet with the first
    two pages being the two inner sides of the innermost sheet, the next two pages
    being the two inner sides of the next sheet, and so on, and the second half of
    the pages being the back sides of the sheets in reverse order.


    Parameters
    ----------
    i
        Position of the page in the input PDF (0-based).
    N
        Total number of pages in the input PDF.

    Returns
    -------
    int
        True (expected) page number of the page at position i.
    """
    if i < N / 2:
        # Front sides
        if i % 2:
            return int(N / 2 + i)
        else:
            return int(N / 2 - i)
    else:
        # Back sides
        if i % 2:
            return int(i - N / 2)
        else:
            return int(N - (i - N / 2))


def get_ordered_sequence(N: int) -> list[int]:
    """
    Get the sequence of (0-based) input PDF page numbers in the corrected order
    for a booklet with N pages total.

    Parameters
    ----------
    N
        Number of pages in the booklet. Must be even.

    Returns
    -------
    list[int]
        Sequence of (0-based) input PDF page numbers in the corrected order.
    """
    assert not N % 2, f"Number of pages must be even, but was {N=}"
    return [
        *map(
            op.itemgetter(0),
            sorted(((i, n(i, N) - 1) for i in range(0, N)), key=op.itemgetter(1)),
        )
    ]


def reorder_pdf(input_path: Union[str, Path], output_path: Union[str, Path]):
    """
    Reorder the pages of a single scanned booklet PDF.

    Parameters
    ----------
    input_path
        Path to the input PDF.
    output_path
        Path to the output PDF.
    """
    reader = PdfReader(input_path)
    N = len(reader.pages)
    writer = PdfWriter()

    sequence = get_ordered_sequence(N)
    log.debug([x + 1 for x in sequence])
    writer.append(reader, sequence)
    writer.write(output_path)


def reorder_all_pdfs_in_directory(input_dir: Path, output_dir: Path):
    """
    Reorder the pages of all scanned booklet PDFs in a directory.
    Prints stuff to stdout (to be used in CLI).

    Parameters
    ----------
    input_dir
        Path to the directory containing the input PDFs.
    output_dir
        Path to the directory where the output PDFs will be saved.
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    input_paths = [*input_dir.glob("*.pdf")]
    if not input_paths:
        print("No PDFs in current directory. Done.")
        return
    n_skipped = 0
    errors = []
    # for input_path in track(input_paths, "Processing..."):
    for input_path in tqdm(input_paths):
        output_path = output_dir / input_path.name
        if output_path.exists():
            n_skipped += 1
        else:
            try:
                reorder_pdf(input_path=input_path, output_path=output_path)
            except Exception as e:
                errors.append(
                    f'Reordering of {input_path.name} failed, error was "{e}"'
                )
    print(
        f"\n{len(input_paths)} files processed, "
        f"{n_skipped} skipped due to output file existing."
    )
    if errors:
        print(f"\n{len(errors)} file(s) failed processing. See details below:")
        print("\n".join(errors))
        print()
