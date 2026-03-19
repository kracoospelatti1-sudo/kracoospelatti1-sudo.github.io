Backups del proyecto EventWall

Esta carpeta guarda copias manuales de seguridad de los archivos principales del sitio.

Backup actual:
- Carpeta: `20260318_180952`
- Motivo: resguardo manual despues de corregir regresiones de encoding y estabilizar `admin.html` / `screen.html`

Contenido del backup:
- `admin.html`
- `guest.html`
- `index.html`
- `screen.html`
- `CHANGELOG.md`

Como restaurar:
1. Elegir la carpeta del backup que quieras usar.
2. Copiar los archivos necesarios desde esa carpeta a la raiz del repo.
3. Revisar `git diff` antes de commitear.

Nota:
- Estos backups no reemplazan a Git.
- Sirven como punto de recuperacion rapido si un archivo HTML grande queda roto por ediciones o problemas de encoding.
