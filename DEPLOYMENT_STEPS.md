# Pasos para Deployment - Mac Cleaner

Este documento te guía paso a paso para subir el proyecto a GitHub, configurar protecciones, y publicarlo en PyPI.

## ✅ Ya Completado

- ✅ Repositorio Git inicializado
- ✅ Commit inicial creado
- ✅ Remote configurado para https://github.com/nmlemus/mac-cleaner.git
- ✅ Botón Buy Me a Coffee agregado al README
- ✅ URLs actualizadas en pyproject.toml

## 📋 Paso 1: Crear el Repositorio en GitHub

1. Ve a https://github.com/new
2. Configura el repositorio:
   - **Repository name**: `mac-cleaner`
   - **Description**: `A safe and intelligent disk cleaning utility for macOS`
   - **Public** o **Private**: Tu elección (recomiendo Public para PyPI)
   - ⚠️ **NO** marques "Initialize this repository with a README" (ya tenemos uno)
   - ⚠️ **NO** agregues .gitignore ni LICENSE (ya los tenemos)
3. Click en "Create repository"

## 📤 Paso 2: Subir el Código a GitHub

Una vez creado el repositorio en GitHub, ejecuta:

```bash
cd /Users/nmlemus/projects/aiudalabs.com/mac_clean

# Push inicial al repositorio
git push -u origin main
```

Si te pide autenticación:
- Usuario: `nmlemus`
- Token: Usa un Personal Access Token (no la contraseña)
  - Crear token: https://github.com/settings/tokens/new
  - Selecciona scopes: `repo` (full control of private repositories)

## 🔒 Paso 3: Proteger el Branch Main

Una vez que el código esté en GitHub:

1. Ve a tu repositorio: https://github.com/nmlemus/mac-cleaner
2. Click en **Settings** (arriba a la derecha)
3. En el menú lateral izquierdo, click en **Branches**
4. En "Branch protection rules", click **Add rule**
5. Configura la protección:

   **Branch name pattern**: `main`

   **Marca estas opciones**:
   - ✅ Require a pull request before merging
     - ✅ Require approvals: 1 (o 0 si trabajas solo)
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging (si tienes CI/CD)
   - ✅ Require conversation resolution before merging
   - ✅ Require linear history (opcional, mantiene el historial limpio)
   - ✅ Include administrators (te protege incluso a ti de push directos)

6. Click **Create** al final

### Alternativa Rápida (Solo prevenir push directo)

Si solo quieres prevenir push directo a main:

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Solo marca:
   - ✅ Require a pull request before merging
   - ✅ Include administrators
4. Create

## 🏷️ Paso 4: Crear Release en GitHub (Opcional pero Recomendado)

```bash
# Crear tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial public release"

# Push tag
git push origin v1.0.0
```

Luego en GitHub:
1. Ve a https://github.com/nmlemus/mac-cleaner/releases/new
2. Select tag: `v1.0.0`
3. Release title: `Mac Cleaner v1.0.0`
4. Describe this release:
   ```markdown
   ## Mac Cleaner v1.0.0 - Initial Release 🧹

   A safe and intelligent disk cleaning utility for macOS.

   ### Features
   - Smart categorization of cleanable files
   - Built-in safety protections
   - Interactive CLI
   - Dry-run mode
   - Multi-language support (English/Spanish)
   - Auto-detects system language

   ### Installation
   ```bash
   pip install mac-cleaner
   ```

   ### Usage
   ```bash
   mac-cleaner --dry-run  # Preview without deleting
   mac-cleaner            # Interactive cleanup
   ```

   ### Support
   If you find this useful, consider [buying me a coffee](https://www.buymeacoffee.com/nmlemus) ☕
   ```
5. Click **Publish release**

## 📦 Paso 5: Construir el Paquete

```bash
cd /Users/nmlemus/projects/aiudalabs.com/mac_clean

# Instalar herramientas de build
pip install --upgrade build twine

# Limpiar builds anteriores (si existen)
rm -rf dist/ build/ *.egg-info

# Verificar que las traducciones estén compiladas
python compile_translations.py

# Construir el paquete
python -m build
```

Esto creará:
- `dist/mac-cleaner-1.0.0.tar.gz` (source distribution)
- `dist/mac_cleaner-1.0.0-py3-none-any.whl` (wheel)

### Verificar el Paquete

```bash
# Verificar que el paquete esté bien formado
python -m twine check dist/*

# Debería decir: "Checking dist/... PASSED"
```

## 🧪 Paso 6: Probar en TestPyPI (Recomendado)

Antes de publicar en PyPI real, prueba en TestPyPI:

### 6.1 Crear Cuenta en TestPyPI

1. Ve a https://test.pypi.org/account/register/
2. Verifica tu email

### 6.2 Crear API Token para TestPyPI

1. Ve a https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `mac-cleaner-upload`
4. Scope: "Entire account"
5. Copia el token (empieza con `pypi-`)

### 6.3 Configurar Credenciales

Crea o edita `~/.pypirc`:

```bash
cat > ~/.pypirc << 'EOF'
[testpypi]
  username = __token__
  password = pypi-TU_TOKEN_DE_TESTPYPI_AQUI

[pypi]
  username = __token__
  password = pypi-TU_TOKEN_DE_PYPI_AQUI_CUANDO_LO_TENGAS
EOF

chmod 600 ~/.pypirc
```

### 6.4 Upload a TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### 6.5 Probar Instalación desde TestPyPI

```bash
# Crear un entorno virtual para probar
python -m venv test_env
source test_env/bin/activate

# Instalar desde TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps mac-cleaner

# Probar
mac-cleaner --help
mac-cleaner --dry-run

# Limpiar
deactivate
rm -rf test_env
```

## 🚀 Paso 7: Publicar en PyPI Real

### 7.1 Crear Cuenta en PyPI

1. Ve a https://pypi.org/account/register/
2. Verifica tu email

### 7.2 Crear API Token para PyPI

1. Ve a https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `mac-cleaner-upload`
4. Scope: "Entire account" (la primera vez, luego puedes hacerlo específico)
5. Copia el token y agrégalo a `~/.pypirc`

### 7.3 Upload a PyPI

```bash
python -m twine upload dist/*
```

### 7.4 Verificar en PyPI

1. Ve a https://pypi.org/project/mac-cleaner/
2. Verifica que toda la información se vea correcta

### 7.5 Probar Instalación

```bash
# Crear entorno limpio
python -m venv test_pypi
source test_pypi/bin/activate

# Instalar desde PyPI
pip install mac-cleaner

# Probar
mac-cleaner --version
mac-cleaner --help
mac-cleaner --dry-run

# Limpiar
deactivate
rm -rf test_pypi
```

## 📢 Paso 8: Anunciar el Release

### Actualizar README en GitHub

El README ya tiene el botón de Buy Me a Coffee y toda la información necesaria.

### Compartir (Opcional)

- Twitter/X
- Reddit (r/MacOS, r/Python, r/opensource)
- Hacker News
- Dev.to

Ejemplo de mensaje:
```
🧹 Just released Mac Cleaner v1.0.0!

A safe & intelligent disk cleaning utility for macOS with:
✅ Smart categorization
✅ Built-in safety protections
✅ Auto language detection (EN/ES)
✅ Dry-run mode

pip install mac-cleaner

⭐ https://github.com/nmlemus/mac-cleaner
☕ https://www.buymeacoffee.com/nmlemus
```

## 🔄 Actualizaciones Futuras

Para publicar actualizaciones:

1. **Hacer cambios en una rama**
   ```bash
   git checkout -b feature/nueva-caracteristica
   # ... hacer cambios ...
   git commit -m "Add: nueva característica"
   git push origin feature/nueva-caracteristica
   ```

2. **Crear Pull Request** en GitHub y hacer merge a main

3. **Actualizar versión**
   - En `pyproject.toml`
   - En `mac_cleaner/__init__.py`

4. **Crear tag y release**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

5. **Rebuild y republish**
   ```bash
   rm -rf dist/
   python -m build
   python -m twine upload dist/*
   ```

## ✅ Checklist Final

Antes de publicar en PyPI, verifica:

- [ ] Repositorio creado en GitHub
- [ ] Código subido a GitHub
- [ ] Branch main protegido
- [ ] Release v1.0.0 creado en GitHub
- [ ] Paquete construido (`python -m build`)
- [ ] Paquete verificado (`twine check dist/*`)
- [ ] Probado en TestPyPI
- [ ] API token de PyPI configurado
- [ ] README se ve bien en GitHub
- [ ] Botón Buy Me a Coffee funciona

## 🆘 Troubleshooting

### Error: "Repository already exists"
Ya existe en GitHub, usa `git push -u origin main` directamente.

### Error: "Authentication failed"
Usa un Personal Access Token en lugar de contraseña:
https://github.com/settings/tokens/new

### Error: "Package already exists" en PyPI
No puedes subir la misma versión dos veces. Incrementa la versión.

### Error: "README rendering failed"
Ejecuta: `python -m twine check dist/*` y corrige los errores.

## 📞 Soporte

Si tienes problemas:
1. Revisa los issues en: https://github.com/nmlemus/mac-cleaner/issues
2. Crea un nuevo issue si es necesario
3. O contáctame en: https://www.buymeacoffee.com/nmlemus

---

**¡Buena suerte con el deployment! 🚀**
