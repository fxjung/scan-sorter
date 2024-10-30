# Scan Sorter

Little utility to reorder PDFs from scanned booklets.

Globs the current working directory for PDF files, then reorders them accordingly. Stores the result in a subdirectory "sorted".
Expected input order for a single-sheet "booklet" is [U2, U3, U4, U1]. I.e., scan the
front side(s), flip around the short (sheet) axis, scan the back side(s).


## Installation

Requires Python >= 3.10

### Option 1

```bash
pip install "scan-sorter@git+https://github.com/fxjung/scan-sorter"
```

### Option 2 (development)

```bash
git clone git@github.com:fxjung/scan-sorter.git
cd scan-sorter
pip install -e .[dev,doc]
```

## Usage

- Change into the directory containing the PDFs
- Execute `scan-sorter`

