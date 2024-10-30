import typer
import logging

from pathlib import Path

from scan_sorter.sorting import reorder_all_pdfs_in_directory

log = logging.getLogger(__name__)


app = typer.Typer()


@app.command()
def sort():
    """
    Sort scanned booklets PDFs
    """

    input_dir = Path.cwd()
    output_dir = input_dir / "sorted"

    reorder_all_pdfs_in_directory(input_dir=input_dir, output_dir=output_dir)
