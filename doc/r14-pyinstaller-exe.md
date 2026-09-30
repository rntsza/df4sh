# Executável Windows (PyInstaller)

## Requisito

Windows, Python 3.11+ com o projeto instalado em modo editable (`pip install -e ".[dev]"`) ou dependências satisfeitas.

## Dependência de empacotamento

```text
pip install ".[bundle]"
```

ou `pip install "pyinstaller>=6"`.

## Construir

Na **raiz do repositório** (pasta que contém `src/` e `df4sh.spec`):

```text
python -m PyInstaller df4sh.spec --noconfirm
```

Saída: **`dist/df4sh.exe`** (one-file, **consola** activa para erros e subcomandos `probe`/`run`).

- **`console=True`** no `.spec`: ao usar só `gui`, podes editar o `.spec` e passar `console=False` para não abrir janela de consola (avisos no messagebox perdem-se no stderr).

## O que vai dentro do .exe

- `config.example.json` e todos os **`*.png`** na raiz do repo (templates configuráveis por defeito).
- Artefactos `cv2` via `collect_all("cv2")`.
- Hidden imports pywin32 comuns.

## Pasta de trabalho em runtime

Com `sys.frozen` (PyInstaller), `resolve_repo_root()`:

1. **`DF4SH_REPO_ROOT`** (se definido e válido).
2. Pasta do **`.exe`** se lá existir `.config` ou `config.example.json`.
3. Caso contrário **`sys._MEIPASS`** (ficheiros embutidos no one-file).

Para config e PNG **editáveis** sem reconstruir: coloca **`df4sh.exe`**, **`.config`** (opcional) e os **PNG** referenciados no JSON **na mesma pasta** que o executável; essa pasta passa a ser a raiz lógica.

## Abrir a GUI

- **Duplo clique** no `df4sh.exe` (PyInstaller): o programa injecta `gui` quando `len(sys.argv)==1`, portanto abre a janela **sem** passares argumentos.
- Manualmente: **`df4sh.exe gui`**
- Consola / probe / run: **`df4sh.exe probe`**, **`df4sh.exe run`**

`python -m df4sh` (não frozen) continua com defeito **`probe`** se não houver subcomando.

## Nota sobre `SPECPATH` no PyInstaller

No `.spec`, **`SPECPATH`** é o **directório** onde está o ficheiro `.spec`, não o caminho completo do ficheiro (`build_main.py` faz `split` do `spec`). O `df4sh.spec` usa isso em `_find_repo_root()`.

## Limpeza local

Pastas geradas: `build/`, `dist/` — convém ignorá-las no git (já em `.gitignore` se listadas).
