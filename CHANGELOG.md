# EventWall — Changelog

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `admin.html` | Panel admin master (PIN). Gestiona eventos, moderación, diseño, links/QR, álbum |
| `guest.html` | Vista del invitado. Subir fotos (frames/filtros/stickers), mensajes, audio, deseos, votar |
| `screen.html` | Vista TV. Muestra posts, carrusel de fotos, deseos, reacciones |
| `index.html` | Landing page pública |

**Stack:** Vanilla JS + HTML/CSS · Supabase (REST API + Storage bucket `eventwall`) · GitHub Pages

---

## Auth

- **Admin master:** `sessionStorage.ew_unlocked === '1'` sin `ew_restricted_event`
- **Cliente restringido:** `sessionStorage.ew_restricted_event = <UUID>` — solo ve su evento, sin editar/borrar
- **PIN de invitados:** campo `admin_pin` en evento, con `pin_expires_at` opcional

## Event ID / custom_code

- Eventos tienen UUID como PK (`id`), usado como FK en todas las tablas
- Columna `custom_code` (text, UNIQUE, nullable) en tabla `events`
- URLs soportan ambos: `?event=boda-caro` o `?event=<uuid>`
- `eventId` es `let` y se reasigna a `ev.id` (UUID) tras el lookup del evento

## Álbum por email

- Al vencer PIN → envío automático del álbum → guarda `localStorage.ew_album_sent_<id>`
- Al borrar evento → verifica `alreadySent` para no duplicar
- PDF adjunto generado con `pdf-lib` en Edge Function `send-album-email`

---

## Base de datos — Tablas relevantes

### reactions
```sql
id uuid PK,
post_id uuid NOT NULL,
event_id text nullable,
emoji text NOT NULL,
guest_name text NOT NULL,
created_at timestamptz,
UNIQUE(post_id, guest_name)  -- una reacción por foto por persona
```
`GRANT SELECT, INSERT, DELETE ON reactions TO anon, authenticated`

---

## Changelog

### 2026-03-16 — Sesión 1

**Reacciones en fotos**
- Nueva tabla `reactions` en Supabase con `UNIQUE(post_id, guest_name)`
- guest.html: tab "Galería" con todas las fotos del evento + botones ❤️🎉😍🔥
- Una reacción por foto por persona — cambiar emoji reemplaza el anterior
- screen.html: pills de reacciones en foto featured, actualizadas cada 5s, fade suave entre fotos

**Landing page (index.html)**
- Testimonios rediseñados: featured quote + 2 cards estáticas (Swiper eliminado)
- Removido: sección galería, hero mockup desktop, botón "Ver demo en vivo", wa-float duplicado
- Limpieza: Swiper CDN, CSS huérfano, doble `const nav`, sp-wrap duplicado
- FAQ schema sincronizado con HTML

**screen.html**
- Fix carrusel: `featuredIdx` se recalcula por ID al llegar foto nueva
- Reacciones con fade in/out entre cambios de foto, sin animación en polls periódicos

**admin.html**
- URL de pantalla ya no desborda el card (`word-break:break-all`)

**guest.html**
- Tab "Galería" con sistema de reacciones completo
- Tab "Votar" permanentemente oculto (votación aparece automática desde admin)
- Tabs: fade gradient derecha + peek animation para indicar scroll horizontal

---

### 2026-03-16 — Sesión 2

- Sonido por defecto cambiado a `none` en screen.html
- "Mis fotos": badge de reacciones por emoji con conteos reales (❤️2 🎉1 🔥3)
- screen.html: fix fade reacciones entre fotos (sin `setTimeout` que borraba el contenido)

---

### 2026-03-16 — Sesión 3

**admin.html — Tab ⚙️ Funciones (Vista invitado)**
- CSS agregado para `.opt-toggle` / `.opt-track` / `.opt-thumb` (switches rosados/grises animados)
- `onclick` movido al `<label>` para que toda la fila sea clickeable
- Nuevos toggles: ❤️ Reacciones en fotos (`showReactions`), 🎨 Personalización de foto (`showPhotoEdit`)
- `GD_DEFAULTS`, `saveGuestDesign`, `showGuestDesign` actualizados
- Tarjetas de eventos: badge rosa `🔗 custom_code` si tiene código personalizado, gris con primeros 8 chars del UUID si no

**guest.html**
- `gdFlags = {showReactions, showPhotoEdit}` actualizado por `applyGuestDesign`
- Selector corregido: `.gallery-reactions` (era `.rxn-btns`)
- Pickers (frame/filter/sticker) solo se muestran si `gdFlags.showPhotoEdit === true`
- Cards de galería sin `.gallery-reactions` si `gdFlags.showReactions === false`

**index.html**
- Card de feature "⚙️ Control total de funciones" en sección Funcionalidades
- "✓ Control de funciones por evento" en pricing checklist

---

### 2026-03-16 — Sesión 4

**admin.html**
- Nuevo toggle `🗑 Borrar fotos propias` (`showDeletePhoto`) en ⚙️ Funciones
- Fix card "Código del evento": `flex-wrap`, font `clamp(28px,5vw,52px)`, botón `white-space:nowrap`, URL `overflow-wrap:anywhere`, `min-width:0` en contenedor flex

**guest.html**
- `gdFlags.showDeletePhoto` actualizado por `applyGuestDesign`
- Botón "🗑 Eliminar" en "Mis fotos" solo se renderiza si `showDeletePhoto === true`

**screen.html**
- Eliminada llamada `playSound(cfg.sound)` del handler de nuevo post — pantalla ya no hace ruido

---

### 2026-03-16 — Sesión 5

**Marca de agua (watermark)**

*admin.html:*
- Sección "Marca de agua" en tab Estilo: file input (PNG/SVG/WebP), posición (tl/tr/bl/br/center), tamaño (5–50%), opacidad (10–100%)
- `uploadWatermark(input)` — sube a `watermarks/{eventId}/wm.{ext}` en bucket `eventwall`
- `removeWatermark()` — limpia URL y oculta preview
- `saveGuestDesign` / `showGuestDesign` incluyen `wmUrl`, `wmPos`, `wmSize`, `wmOpacity`
- Fix: `BUCKET` no está definido en admin.html → reemplazado con literal `'eventwall'`

*guest.html:*
- `gdFlags` extendido con `wmUrl`, `wmPos`, `wmSize`, `wmOpacity`
- `_wmImage` — `Image()` cacheada con `crossOrigin='anonymous'`; no recarga si URL no cambió
- `img.onload` re-renderiza el canvas si ya hay foto seleccionada
- Watermark dibujada al final de `renderPreviewCanvas()` con `ctx.globalAlpha` + `ctx.drawImage`
- `sendPhoto()` llama `renderPreviewCanvas()` antes de `canvas.toBlob()` para garantizar que la marca esté quemada en el JPEG

*screen.html:*
- `<img id="screen-wm">` overlay absoluto sobre `#featured-img` (z-index:5, pointer-events:none)
- `applyScreenWatermark(gd)` — posiciona y opacifica el overlay según config
- `init()` carga `guest_design` y llama `applyScreenWatermark`

**Plantillas de pantalla (5 nuevas)**
- `TEMPLATES` + `applyTemplate` en admin.html: `xv` (XV Años), `corporate` (Corporativo), `birthday` (Cumpleaños), `boho` (Boho), `sunset` (Sunset)

**Plantillas de diseño invitado (10 presets)**
- Tab "🎨 Plantillas" (primero) en config de Vista invitado, 10 cards con mini hero preview
- `applyGDTemplate(name)` — aplica colores + fonts por preset

**"Quién reaccionó" popover**
- guest.html: toque largo (500ms) o click derecho en botón de reacción → popover con nombres
- `showRxnPopover(e, btn, emoji)` — singleton div, posicionado con `getBoundingClientRect()`
- `rxnMap` restructurado: `{count, names:[]}` por emoji por post
- `renderGalleryCard` pasa `data-rxn-names` (JSON) en cada botón

**Fechas en formato DD/MM/AAAA**
- `formatDateES(str)` — convierte `YYYY-MM-DD` → `DD/MM/AAAA`
- Aplicado en `ev-sub` de guest.html y screen.html

**index.html — Formulario de contacto**
- Campo fecha: `type="text"` con `maskDate(el)` (inserta `/` automático en pos 2 y 5)
- Labels: sin uppercase/letter-spacing, `font-size:13px`, emojis (👤🎉📅👥💬)
- "Cantidad estimada de invitados" → "Cantidad de invitados"

**Carrusel — nueva foto va al frente de la cola**
- Foto nueva se inserta en `photoPosts` justo después de la foto actual (`splice(insertAt, 0, p)`)
- En la próxima rotación, la foto nueva es la primera en aparecer
- Si no hay fotos todavía, aparece de inmediato

---

### Sesiones anteriores (resumen)

- PDF adjunto al email del álbum (Edge Function con pdf-lib en Deno)
- AOS.js animaciones scroll en landing, marquee infinito proof bar
- Announcement bar, mobile menu fix, countdown dinámico, nav active en index
- Moderación integrada en panel Contenido del admin
- Sidebar configurable en screen (ancho, visibilidad)
- Eliminación instantánea de mensajes/deseos en screen al moderar desde admin
