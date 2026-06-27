# Building Systems Under Constraints

This repository contains a small ecosystem of tools built to solve a simple problem:

**How do you continue reading English web novels when your available hardware was never designed for it?**

---

## The Constraint

In 2026, I lost normal access to a computer.

The hardware that remained available was:

- A keypad phone with a 30 GB SD card.
- An old offline television.
- Occasional short periods of computer access.

The television could:

- Display JPG images.
- Play MP4 files.
- Read data from USB and SD cards.

The television could not:

- Open PDF files.
- Connect to the internet.
- Function as an ebook reader.

At the time I was already reading English web novels regularly and wanted to continue doing so.

Stopping was one option.

Building around the limitation became another.

I chose the second.

---

## The First Solution

The television could display JPG files.

That meant the target format became images.

The first tool in this repository was therefore a PDF to JPG converter.

Its purpose was simple:

```
PDF
↓
Thousands of JPG images
↓
SD card
↓
Television
```

This immediately introduced a new problem.

Television remotes are extremely inefficient at navigating thousands of files inside a single folder.

The solution was a hierarchical folder structure.

Instead of:

```
Novel/
    page_1.jpg
    page_2.jpg
    ...
    page_10000.jpg
```

The generated structure became:

```
Novel/
│
├── 1-1000/
│   ├── 1-100/
│   │   ├── 1-10/
│   │   │   ├── 1.jpg
│   │   │   ├── 2.jpg
│   │   │   └── ...
│   │   └── ...
│   └── ...
└── ...
```

This reduced navigation time dramatically when using only directional buttons on a remote control.

The television became a usable ebook reader.

---

## The Second Problem

Eventually the available PDF sources became insufficient.

Many novels simply did not exist in downloadable PDF form.

The limitation moved.

The system evolved.

---

## The Pipeline

Three tools eventually emerged.

### pwnlg.py

**Python Web Novel Link Generator**

This tool generates chapter URLs automatically.

Example:

```
chapter-1
chapter-2
chapter-3
...
chapter-1000
```

The resulting links are stored inside a text file.

---

### pwnpcu.py

**Python Web Novel PDF Creator Utilized**

This tool reads the generated link file.

For each chapter it:

1. Downloads the webpage.
2. Extracts the actual chapter text.
3. Removes unnecessary content.
4. Combines all chapters together.
5. Produces a PDF file.

Pipeline:

```
URLs
↓
Web pages
↓
Chapter extraction
↓
Single PDF
```

---

### pdc.py

**PDF Deconstructor / Converter**

This tool converts the generated PDF into JPG images.

It then creates the nested folder structure required for practical navigation using a television remote.

Pipeline:

```
PDF
↓
Images
↓
Hierarchical folders
↓
SD card
↓
Television
```

---

## Complete Architecture

```
Web Novel Website
        ↓
pwnlg.py
        ↓
Chapter URL List
        ↓
pwnpcu.py
        ↓
PDF File
        ↓
pdc.py
        ↓
Nested JPG Structure
        ↓
SD Card
        ↓
Television
        ↓
Reading
```

---

## Deployment

This was not an experiment.

This became my primary reading system.

The system was actively used for more than a year.

Approximate scale:

- Around 30 novels processed.
- Approximately 150,000 pages generated.
- Roughly 10,000 pages personally read through this pipeline.
- Approximately 800 chapters consumed using this workflow.

The television effectively became an ebook reader.

The keypad phone became a transport medium and storage device.

The software became the bridge between them.

---

## Design Philosophy

Most software projects begin with available resources.

This one began with unavailable resources.

Every design decision originated from a constraint:

| Constraint | Result |
|------------|--------|
| No internet on TV | Offline workflow |
| No PDF support | JPG conversion |
| Slow remote navigation | Hierarchical folders |
| Limited computer access | Automation |
| Lack of downloadable PDFs | Scraping pipeline |

The constraints did not merely limit the design.

They created it.

---

## Lessons Learned

This project taught me several things:

- Constraints often produce better architecture.
- Hardware limitations can become software problems.
- Interfaces should be designed around the input device available to the user.
- Practical systems matter more than elegant systems.
- A tool only needs to solve one problem extremely well to become valuable.

---

## Repository Structure

```
ReadingUnderConstraints/
│
├── pwnlg.py
├── pwnpcu.py
├── pdc.py
└── README.md
```

---

## Status

This project is complete.

It solved the problem it was designed to solve.

Although the original environment that required it no longer exists, the project remains an example of building systems under severe constraints using whatever hardware was available.

---

## Final Observation

The original objective was never to build software.

The objective was simply:

```
Continue reading.
```

Everything else emerged from that requirement.