# Quick Start Guide / Guía Rápida

## English

### Installation

```bash
# Install from source
pip install .

# Or install in development mode
pip install -e .
```

### Usage

```bash
# Run the cleaner
mac-cleaner

# Preview without deleting (recommended for first run)
mac-cleaner --dry-run

# Check version
mac-cleaner --version
```

### First Run Recommendations

1. **Always start with dry-run**:
   ```bash
   mac-cleaner --dry-run
   ```
   This shows you what would be deleted without actually deleting anything.

2. **Review the categories carefully** - Make sure you understand what each category contains.

3. **Start with safe categories** - Browser caches and temporary files are usually safe to delete.

4. **Be careful with**:
   - Node Modules (you'll need to run `npm install` again in those projects)
   - Development Caches (might slow down next build)
   - Docker Data (will need to re-pull images)

### Example Session

```bash
$ mac-cleaner
Scanning categories...
Categories found:
 1) Temporary Files               2.3 GB (4 items)
 2) System Log Files              856.2 MB (3 items)
 3) Browser Cache                 1.2 GB (5 items)
 4) Node Modules                  4.5 GB (12 items)
 5) Development Cache             3.1 GB (6 items)

Select categories (e.g., 1,3,5 or all):
> 1,2,3

Summary:
- /tmp  1.5 GB
- /var/log  856.2 MB
- ~/Library/Caches/Google/Chrome  1.2 GB
Total: 3.5 GB

Delete all of the above? [y/N]: y

Starting deletion...
✓ Deleted: /tmp
✓ Deleted: /var/log
✓ Deleted: ~/Library/Caches/Google/Chrome

Cleanup completed.
```

---

## Español

### Instalación

```bash
# Instalar desde el código fuente
pip install .

# O instalar en modo desarrollo
pip install -e .
```

### Uso

```bash
# Ejecutar el limpiador
mac-cleaner

# Previsualizar sin borrar (recomendado para primera ejecución)
mac-cleaner --dry-run

# Ver versión
mac-cleaner --version
```

### Recomendaciones para Primera Ejecución

1. **Siempre empieza con dry-run**:
   ```bash
   mac-cleaner --dry-run
   ```
   Esto te muestra qué se borraría sin borrar nada realmente.

2. **Revisa las categorías cuidadosamente** - Asegúrate de entender qué contiene cada categoría.

3. **Empieza con categorías seguras** - Los cachés de navegadores y archivos temporales son generalmente seguros de borrar.

4. **Ten cuidado con**:
   - Node Modules (necesitarás ejecutar `npm install` de nuevo en esos proyectos)
   - Cachés de Desarrollo (podría hacer más lenta la próxima compilación)
   - Datos de Docker (necesitarás volver a descargar las imágenes)

### Sesión de Ejemplo

```bash
$ mac-cleaner
Escaneando categorías...
Categorías encontradas:
 1) Archivos Temporales           2.3 GB (4 items)
 2) Archivos de Log del Sistema   856.2 MB (3 items)
 3) Caché de Navegadores          1.2 GB (5 items)
 4) Node Modules                  4.5 GB (12 items)
 5) Caché de Desarrollo           3.1 GB (6 items)

Selecciona categorías (ej: 1,3,5 o all):
> 1,2,3

Resumen:
- /tmp  1.5 GB
- /var/log  856.2 MB
- ~/Library/Caches/Google/Chrome  1.2 GB
Total: 3.5 GB

¿Eliminar todo lo anterior? [y/N]: y

Iniciando borrado...
✓ Borrado: /tmp
✓ Borrado: /var/log
✓ Borrado: ~/Library/Caches/Google/Chrome

Limpieza completada.
```

## Tips

### English
- Run `mac-cleaner` regularly (monthly) to keep your system clean
- Use `--dry-run` when trying new categories
- Docker cleanup is safe but you'll need to re-download images
- Node modules can be reinstalled with `npm install` or `yarn install`

### Español
- Ejecuta `mac-cleaner` regularmente (mensualmente) para mantener tu sistema limpio
- Usa `--dry-run` cuando pruebes nuevas categorías
- La limpieza de Docker es segura pero necesitarás volver a descargar las imágenes
- Los node modules pueden reinstalarse con `npm install` o `yarn install`
