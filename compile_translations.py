#!/usr/bin/env python3
"""
Compile .po files to .mo files for gettext.
Run this script whenever you update translations.
"""

import subprocess
from pathlib import Path


def compile_po_file(po_file: Path) -> None:
    """Compile a single .po file to .mo format."""
    mo_file = po_file.with_suffix('.mo')
    print(f"Compiling {po_file} -> {mo_file}")

    try:
        subprocess.run(
            ['msgfmt', str(po_file), '-o', str(mo_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  ✓ Success")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed: {e.stderr}")
    except FileNotFoundError:
        print("  ✗ msgfmt not found. Please install gettext:")
        print("    brew install gettext")
        print("    Then add to PATH: export PATH=\"/opt/homebrew/opt/gettext/bin:$PATH\"")


def main():
    """Find and compile all .po files."""
    locales_dir = Path(__file__).parent / 'mac_cleaner' / 'locales'

    po_files = list(locales_dir.rglob('*.po'))

    if not po_files:
        print("No .po files found!")
        return

    print(f"Found {len(po_files)} translation file(s)\n")

    for po_file in po_files:
        compile_po_file(po_file)

    print("\nDone!")


if __name__ == '__main__':
    main()
