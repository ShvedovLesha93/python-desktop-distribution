# Python Desktop Distribution

A sample `PySide6` application demonstrating how to build cross-platform desktop applications
with internationalization (i18n) support using a lightweight `uv`-based bootstrap launcher.

## How it works

Instead of bundling all libraries into a large exe, `PyInstaller` only packages a small launcher.
On first run, the launcher uses `uv` to download and install all dependencies
into a local `.venv` next to the executable. Subsequent launches skip this step entirely.
The final installer is built with [Inno Setup](https://jrsoftware.org/isinfo.php).

## Features

- ✨ Simple `PySide6` GUI with language switching
- 🌍 Internationalization support using `gettext`
- 🔄 Runtime language switching between English and Russian
- 📦 Lightweight launcher — only a small exe is shipped, dependencies are fetched on first run
- 🚀 Fully isolated environment — `uv` manages its own Python, no system Python required

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/ShvedovLesha93/python-desktop-distribution.git
cd learning-pyinstaller

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/ShvedovLesha93/python-desktop-distribution.git
cd learning-pyinstaller

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install PySide6 pyinstaller
```

## Running in Development

```bash
# Using UV
uv run python main.py

# Using regular Python
python main.py
```

## Adding New Translations

### 1. Extract translatable strings

```bash
uv run python i18n_extract.py
```

### 2. Create or update language files

For a new language (e.g., French):

```bash
mkdir -p app/locales/fr/LC_MESSAGES
msginit -i app/locales/messages.pot \
    -o app/locales/fr/LC_MESSAGES/messages.po \
    -l fr
```

For updating existing translations:

```bash
msgmerge -U app/locales/ru/LC_MESSAGES/messages.po app/locales/messages.pot
```

### 3. Edit the .po file

Open `app/locales/ru/LC_MESSAGES/messages.po` and add translations:

```po
msgid "Change language"
msgstr "Изменить язык"

msgid "Language changed to: {lang}"
msgstr "Язык изменён на: {lang}"
```

### 4. Compile translations

```bash
msgfmt app/locales/ru/LC_MESSAGES/messages.po \
    -o app/locales/ru/LC_MESSAGES/messages.mo
```

### 5. Add language to the app

Update `main.py` to include the new language:

```python
self._languages = ["ru", "en", "fr"]
```

## Building

### 1. Build the launcher and assemble dist

```bash
uv run python build.py
```

The `dist/` folder will be assembled with:

- `MyApp.exe` (Windows) or `MyApp` (Linux) — the launcher (built by PyInstaller, no dependencies bundled)
- App source files, `pyproject.toml`, and `uv.lock`

### 2. Build the installer

```bash
uv run python package.py
```

**Windows** — runs [Inno Setup](https://jrsoftware.org/isinfo.php) via `iscc`
and places `mysetup.exe` in `release/`.

**Linux** — creates `MyApp.tar.gz` in `release/`.

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [GNU gettext Manual](https://www.gnu.org/software/gettext/manual/)
- [PyInstaller Documentation](https://pyinstaller.org/)

## License

This project is created for educational purposes.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions!
