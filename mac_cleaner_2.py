#!/usr/bin/env python3
import os
import shutil
import argparse
import subprocess
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

# =========================
# Colores (ANSI)
# =========================

RESET = "\033[0m"
BOLD = "\033[1m"

FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_BLUE = "\033[34m"
FG_CYAN = "\033[36m"
FG_MAGENTA = "\033[35m"
FG_GRAY = "\033[90m"

def color(text: str, c: str) -> str:
    return f"{c}{text}{RESET}"

def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"

# =========================
# Helpers
# =========================

def expand(p: str) -> Path:
    return Path(os.path.expanduser(p))

def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for u in units:
        if size < 1024.0:
            return f"{size:.1f} {u}"
        size /= 1024.0
    return f"{size:.1f} PB"

def parse_docker_size(size_str: str) -> int:
    m = re.match(r"([\d\.]+)([kMGT]?B)", size_str)
    if not m:
        return 0
    value = float(m.group(1))
    unit = m.group(2)
    multipliers = {
        "B": 1,
        "kB": 1000,
        "MB": 1000**2,
        "GB": 1000**3,
        "TB": 1000**4,
    }
    return int(value * multipliers.get(unit, 1))

def docker_is_running() -> bool:
    """Devuelve True si Docker está corriendo y responde."""
    if shutil.which("docker") is None:
        return False
    try:
        subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1,
            check=True
        )
        return True
    except Exception:
        return False

@dataclass
class PathItem:
    path: Path
    size_bytes: int
    file_count: int

@dataclass
class Category:
    name: str
    description: str
    items: List[PathItem] = field(default_factory=list)

    @property
    def total_size(self) -> int:
        return sum(i.size_bytes for i in self.items)

    @property
    def total_files(self) -> int:
        return sum(i.file_count for i in self.items)

# =========================
# Barra de progreso
# =========================

def print_progress_bar(step: int, total: int, prefix: str = "Escaneando", length: int = 30):
    if total <= 0:
        total = 1
    fraction = step / total
    if fraction > 1:
        fraction = 1
    filled = int(length * fraction)
    bar = "█" * filled + " " * (length - filled)
    msg = f"{prefix}: |{bar}| {step}/{total}"
    print("\r" + color(msg, FG_CYAN), end="", flush=True)

# =========================
# Scan logic
# =========================

def safe_walk(path: Path) -> Tuple[int, int]:
    if not path.exists():
        return 0, 0

    if path.is_file():
        try:
            return path.stat().st_size, 1
        except OSError:
            return 0, 0

    total_size = 0
    file_count = 0
    try:
        for root, dirs, files in os.walk(path, followlinks=False):
            dirs[:] = [d for d in dirs if not Path(root, d).is_symlink()]
            for f in files:
                fp = Path(root, f)
                try:
                    total_size += fp.stat().st_size
                    file_count += 1
                except OSError:
                    continue
    except OSError:
        pass
    return total_size, file_count

def add_if_exists(cat: Category, paths: List[Path]) -> None:
    for p in paths:
        if p.exists():
            size, count = safe_walk(p)
            if count > 0 or p.is_file():
                cat.items.append(PathItem(path=p, size_bytes=size, file_count=count))

def find_node_modules_roots(search_roots: List[Path], max_depth: int = 5) -> List[Path]:
    """
    Busca directorios node_modules en algunos roots.
    max_depth limita la profundidad desde cada root para evitar búsquedas eternas.
    """
    found: List[Path] = []
    for root in search_roots:
        if not root.exists():
            continue
        start_depth = len(root.parts)
        for dirpath, dirnames, _ in os.walk(root):
            current_depth = len(Path(dirpath).parts)
            if current_depth - start_depth > max_depth:
                dirnames[:] = []
                continue
            if "node_modules" in dirnames:
                nm_path = Path(dirpath) / "node_modules"
                found.append(nm_path)
                # no seguimos dentro de ese node_modules
                dirnames.remove("node_modules")
    return found

# -------------------------
# Docker
# -------------------------

def get_docker_reclaimable_bytes() -> int:
    if shutil.which("docker") is None:
        return 0
    try:
        proc = subprocess.run(
            ["docker", "system", "df", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception:
        return 0

    total = 0
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            info = json.loads(line)
        except Exception:
            continue
        rec = info.get("Reclaimable", "")
        if not rec or rec.startswith("0B"):
            continue
        first = rec.split()[0]
        total += parse_docker_size(first)
    return total

# -------------------------
# Discover categories
# -------------------------

def discover_categories(progress_cb=None) -> List[Category]:
    categories: List[Category] = []

    planned_total = 8
    step = 0

    # 1) Temporary Files
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    temp_cat = Category("Temporary Files", "Archivos temporales del sistema y apps")
    add_if_exists(temp_cat, [
        Path("/tmp"),
        Path("/var/tmp"),
        Path("/private/var/tmp"),
        Path("/private/var/folders"),
    ])
    categories.append(temp_cat)

    # 2) System Log Files
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    logs_cat = Category("System Log Files", "Logs del sistema y aplicaciones")
    add_if_exists(logs_cat, [
        expand("~/Library/Logs"),
        Path("/var/log"),
        Path("/Library/Logs"),
    ])
    categories.append(logs_cat)

    # 3) Homebrew Cache
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    brew_cat = Category("Homebrew Cache", "Caches y descargas de Homebrew")
    add_if_exists(brew_cat, [
        expand("~/Library/Caches/Homebrew"),
        Path("/Library/Caches/Homebrew"),
        Path("/opt/homebrew/var/homebrew"),
    ])
    categories.append(brew_cat)

    # 4) Browser Cache
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    browser_cat = Category("Browser Cache", "Cache de navegadores")
    add_if_exists(browser_cat, [
        expand("~/Library/Caches/com.apple.Safari"),
        expand("~/Library/Caches/Google/Chrome"),
        expand("~/Library/Caches/Firefox"),
        expand("~/Library/Caches/Mozilla"),
        expand("~/Library/Caches/BraveSoftware"),
        expand("~/Library/Caches/Microsoft Edge"),
    ])
    categories.append(browser_cat)

    # 5) Node Modules
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    node_cat = Category("Node Modules", "node_modules encontrados en proyectos")
    roots = [expand("~/Projects"), expand("~/Documents"), expand("~/workspace"), expand("~/Work")]
    dirs = find_node_modules_roots(roots, max_depth=5)
    add_if_exists(node_cat, dirs)
    categories.append(node_cat)

    # 6) User Cache Files
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    user_cache_cat = Category("User Cache Files", "Caches de usuario (excluyendo com.apple.*)")
    root = expand("~/Library/Caches")
    if root.exists():
        for child in root.iterdir():
            if child.name.startswith("com.apple."):
                continue
            size, files = safe_walk(child)
            if size > 0:
                user_cache_cat.items.append(PathItem(child, size, files))
    categories.append(user_cache_cat)

    # 7) Development Cache
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    dev_cat = Category("Development Cache", "Caches de Xcode, npm, pip, yarn, etc.")
    add_if_exists(dev_cat, [
        expand("~/Library/Developer/Xcode/DerivedData"),
        expand("~/Library/Developer/Xcode/Archives"),
        expand("~/Library/Developer/Xcode/iOS DeviceSupport"),
        expand("~/Library/Caches/CocoaPods"),
        expand("~/.npm"),
        expand("~/.cache/yarn"),
        expand("~/.cache/pip"),
        expand("~/.pnpm-store"),
    ])
    categories.append(dev_cat)

    # 8) Docker Data (with validation)
    step += 1
    if progress_cb: progress_cb(step, planned_total)
    docker_cat = Category("Docker Data", "Imágenes y volúmenes no usados de Docker")

    if not docker_is_running():
        print(color("\n[ADVERTENCIA] Docker no está ejecutándose. "
                    "No se podrá calcular el espacio reclamable.\n", FG_YELLOW))
        reclaimable = 0
    else:
        reclaimable = get_docker_reclaimable_bytes()

    docker_cat.items.append(
        PathItem(path=Path("[Docker]"), size_bytes=reclaimable, file_count=0)
    )
    categories.append(docker_cat)

    return [c for c in categories if c.items]

# =========================
# UI & Cleanup
# =========================

def prompt_select_indices(max_index: int, allow_all: bool = True) -> List[int]:
    while True:
        raw = input(color("> Selección: ", FG_GREEN)).strip().lower()
        if not raw:
            return []
        if allow_all and raw in ("all", "todo", "todos"):
            return list(range(max_index))
        parts = raw.split(",")
        result = []
        ok = True
        for p in parts:
            p = p.strip()
            if not p.isdigit():
                ok = False
                break
            v = int(p) - 1
            if v < 0 or v >= max_index:
                ok = False
                break
            result.append(v)
        if ok:
            return sorted(set(result))
        print(color("Entrada inválida.", FG_RED))

def confirm(prompt: str) -> bool:
    ans = input(color(f"{prompt} [y/N]: ", FG_YELLOW)).strip().lower()
    return ans in ("y", "yes", "s", "si", "sí")

def interactive_cleanup(dry_run: bool = False):
    print(bold(color("Escaneando categorías...", FG_CYAN)))

    categories = discover_categories(progress_cb=print_progress_bar)
    print()

    if not categories:
        print(color("No se encontraron categorías con datos.", FG_YELLOW))
        return

    print("\n" + bold("Categorías encontradas:"))
    for i, cat in enumerate(categories, 1):
        print(color(
            f"{i:2d}) {cat.name:20s}  {human_size(cat.total_size)} ({len(cat.items)} items)",
            FG_BLUE
        ))

    print(color("\nSelecciona categorías (ej: 1,3,5 o all):", FG_GRAY))
    indices = prompt_select_indices(len(categories))

    if not indices:
        print(color("Nada seleccionado.", FG_YELLOW))
        return

    selected_items: List[PathItem] = []
    for idx in indices:
        selected_items.extend(categories[idx].items)

    # Summary
    total = sum(i.size_bytes for i in selected_items)
    print("\n" + bold("=" * 40))
    print(color("Resumen:", FG_CYAN))
    for i in selected_items:
        print(color(f"- {i.path}  {human_size(i.size_bytes)}", FG_BLUE))
    print(color(f"Total: {human_size(total)}", FG_GREEN))
    print(bold("=" * 40))

    if dry_run:
        print(color("Dry-run: no se borrará nada.", FG_YELLOW))
        return

    if not confirm("¿Eliminar todo lo anterior?"):
        print(color("Cancelado.", FG_YELLOW))
        return

    print(color("\nIniciando borrado...", FG_CYAN))

    for item in selected_items:
        p = item.path

        # Caso especial: Docker
        if str(p) == "[Docker]":
            if not docker_is_running():
                print(color("[IGNORADO] Docker no está corriendo, no se ejecutará 'docker system prune'.", FG_YELLOW))
                continue

            print(color("Ejecutando docker system prune -af --volumes...", FG_YELLOW))
            try:
                subprocess.run(
                    ["docker", "system", "prune", "-af", "--volumes"],
                    check=True
                )
                print(color("Docker limpiado.", FG_GREEN))
            except Exception as e:
                print(color(f"[ERROR] Docker prune falló: {e}", FG_RED))
            continue

        # Casos de carpetas/archivos normales
        try:
            if p.name.startswith("com.apple."):
                print(color(f"[IGNORADO] Saltando ruta protegida: {p}", FG_GRAY))
                continue

            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p, ignore_errors=False)
            else:
                p.unlink(missing_ok=True)

            print(color(f"Borrado: {p}", FG_GREEN))

        except PermissionError:
            print(color(f"[IGNORADO] Permisos restringidos: {p}", FG_YELLOW))
        except OSError as e:
            if "Operation not permitted" in str(e):
                print(color(f"[IGNORADO] Protegido por macOS: {p}", FG_GRAY))
            else:
                print(color(f"[ERROR] {p}: {e}", FG_RED))

    print(color("\nLimpieza completada.", FG_GREEN))

# =========================
# Entry
# =========================

def main():
    parser = argparse.ArgumentParser(description="Mac Cleaner CLI mejorado")
    parser.add_argument("--dry-run", action="store_true", help="Simula sin borrar nada")
    args = parser.parse_args()
    interactive_cleanup(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
