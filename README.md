# Mental Calc

A small desktop app that generates printable mental-arithmetic exercise sheets as Word documents — written, in the author's own words, "in order to torment innocent children ;-)"

## What it does

Pick one or more exercise types — addition, subtraction, multiplication, division — and set a number range for each. Mental Calc then produces a `.docx` file with two pages of 51 exercises each, laid out in three columns of large-print problems with a name/date line at the top, ready to print.

To keep things interesting, the blank isn't always at the end: the missing number appears randomly on the left (`___ + 5 = 12`), in the middle (`7 + ___ = 12`), or on the right (`7 + 5 = ___`). Subtraction never goes negative and division always comes out even.

Default ranges are 1–20 for addition/subtraction and 1–10 for multiplication/division, adjustable per exercise type (0–100).

## Download

Prebuilt, self-contained binaries are available on the [Releases](../../releases) page:

| File | Platform |
| --- | --- |
| `MentalCalc.exe` | Windows |
| `MentalCalc-linux-mint22-x86_64` | Linux Mint 22.x / Ubuntu 24.04 (needs GTK3, preinstalled on desktop systems) |

No Python installation required. On Linux, make the file executable first: `chmod +x MentalCalc-linux-mint22-x86_64`

## Running from source

Requires Python 3.10+ with [wxPython](https://wxpython.org/) and [python-docx](https://python-docx.readthedocs.io/):

```
pip install wxPython python-docx
python MentalCalc.py
```

On Linux, install wxPython from the prebuilt wheels to avoid a long source build, e.g. for Ubuntu 24.04:

```
pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04 wxPython
```

`mental_calc.py` (the generator) also works standalone without the GUI: `python mental_calc.py` writes a timestamped sheet with default settings to the current directory.

## Building binaries

Binaries are built with [PyInstaller](https://pyinstaller.org/) using the included spec file:

```
pip install pyinstaller
pyinstaller MentalCalc.spec
```

A GitHub Actions workflow (`.github/workflows/build.yml`) builds both platforms automatically: push a tag like `v1.0` and the binaries are attached to a GitHub Release, or trigger it manually from the Actions tab.

## Project layout

| File | Purpose |
| --- | --- |
| `MentalCalc.py` | wxPython GUI (entry point) |
| `mental_calc.py` | Exercise generator and Word-document output |
| `MentalCalc.spec` | PyInstaller build configuration |
| `.github/workflows/build.yml` | CI builds for Windows and Linux |

## License

MIT — Copyright 2026 Martin Groß <martin@cavedev.de>. See the license header in the source files.
