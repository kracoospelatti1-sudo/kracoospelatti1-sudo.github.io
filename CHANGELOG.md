# EventWall â€” Changelog

## Estructura del proyecto

| Archivo | DescripciÃ³n |
|---|---|
| `admin.html` | Panel admin master (PIN). Gestiona eventos, moderaciÃ³n, diseÃ±o, links/QR, Ã¡lbum |
| `guest.html` | Vista del invitado. Subir fotos (frames/filtros/stickers), mensajes, audio, deseos, votar |
| `screen.html` | Vista TV. Muestra posts, carrusel de fotos, deseos, reacciones |
| `index.html` | Landing page pÃºblica |

**Stack:** Vanilla JS + HTML/CSS Â· Supabase (REST API + Storage bucket `eventwall`) Â· GitHub Pages

---

## Auth

- **Admin master:** valida el PIN maestro contra `app_config.master_pin` al ingresar
- **Persistencia:** ya no se reutiliza `sessionStorage.ew_unlocked` para reabrir el panel al recargar
- **Cliente restringido:** `sessionStorage.ew_restricted_event = <UUID>` â€” solo ve su evento, sin editar/borrar
- **PIN de invitados:** campo `admin_pin` en evento, con `pin_expires_at` opcional

## Event ID / custom_code

- Eventos tienen UUID como PK (`id`), usado como FK en todas las tablas
- Columna `custom_code` (text, UNIQUE, nullable) en tabla `events`
- URLs soportan ambos: `?event=boda-caro` o `?event=<uuid>`
- `eventId` es `let` y se reasigna a `ev.id` (UUID) tras el lookup del evento

## Ãlbum por email

- Al vencer PIN â†’ envÃ­o automÃ¡tico del Ã¡lbum â†’ guarda `localStorage.ew_album_sent_<id>`
- Al borrar evento â†’ verifica `alreadySent` para no duplicar
- PDF adjunto generado con `pdf-lib` en Edge Function `send-album-email`

---

## Base de datos â€” Tablas relevantes

### reactions
```sql
id uuid PK,
post_id uuid NOT NULL,
event_id text nullable,
emoji text NOT NULL,
guest_name text NOT NULL,
created_at timestamptz,
UNIQUE(post_id, guest_name)  -- una reacciÃ³n por foto por persona
```
`GRANT SELECT, INSERT, DELETE ON reactions TO anon, authenticated`

---

## Changelog

### 2026-03-18 - Sesion 8

**Landing / SEO (`index.html`)**
- Se reviso `index.html` y se confirmo que el archivo local coincide byte a byte con una version sana del repo; no fue necesario restaurarlo completo
- Open Graph y Twitter Cards ahora usan `example2.png`, que si existe en el repo, en lugar de `og-image.png`, que no estaba presente
- Se agregaron `og:image:alt`, `twitter:url`, `twitter:image:alt`, `theme-color`, `format-detection` y `robots=max-image-preview:large`
- El JSON-LD de `Service` ahora incluye `image` y `sameAs` hacia Instagram

**Seguridad / higiene**
- Todos los links externos con `target="_blank"` en `index.html` ahora incluyen `rel="noopener noreferrer"`

**Nota operativa**
- Cuando el shell muestre mojibake en archivos HTML grandes, validar primero contra Git antes de reescribir; en este caso el problema visible en consola no implicaba bytes distintos en `index.html`

---

### 2026-03-18 - Sesion 9

**Marca / logo (`index.html`)**
- Se incorporo `eventwall.png` como logo visible de la landing
- Header y footer ahora muestran la imagen de marca junto al texto `EventWall`
- Se reemplazo el punto decorativo anterior por una clase reutilizable `brand-mark`, con tamanos adaptados para navbar y footer

### 2026-03-18 - Sesion 10

**Ajuste visual del logo (`index.html`)**
- El logo de la landing ahora reemplaza el texto `EventWall` en header y footer, en vez de mostrarse a su lado
- Se aumento el tamano visual de `eventwall.png` para que la marca tenga mas presencia en navegacion y pie

---

### 2026-03-18 - Sesion 11

**Reversion del logo en la landing**
- Se quito `eventwall.png` de `index.html`
- Header y footer volvieron al branding anterior: punto rosa + texto `EventWall`
- Se elimina tambien el archivo `eventwall.png` del repo

---

### 2026-03-18 - Sesion 12

**SEO tecnico (`index.html`)**
- Se agregaron `hreflang`, `og:image:secure_url`, `og:image:type` y `meta language` en la landing
- Se sumo schema adicional de `Organization` y `WebSite` para reforzar entidad de marca y contexto del sitio

**Archivos SEO**
- Nuevo `robots.txt` con referencia al sitemap publico
- Nuevo `sitemap.xml` para la URL canonica del sitio

---

### 2026-03-18 - Sesion 13

**Copy SEO de la landing**
- Se reforzo el hero con keywords mas descriptivas como `muro digital para eventos`, `bodas`, `fiestas de 15` y `eventos corporativos`
- Se actualizaron los textos de las secciones `En vivo`, `Como funciona` y `Funcionalidades` para mejorar relevancia semantica sin perder tono comercial

---

### 2026-03-18 - Sesion 14

**Migracion SEO a Hostinger**
- `index.html` ahora usa `darkblue-swallow-842981.hostingersite.com` en `canonical`, `hreflang`, Open Graph, Twitter y schemas
- `robots.txt` y `sitemap.xml` se actualizaron para apuntar al dominio de Hostinger en lugar de GitHub Pages

---

### 2026-03-18 - Sesion 15

**Dominio principal**
- `index.html`, `robots.txt` y `sitemap.xml` ahora usan `https://eventwall.online/` como dominio canonico principal
- Se elimino `CNAME` del repo para que GitHub Pages deje de reclamar `eventwall.online`

---

---

### 2026-03-18 - Sesion 7

**Regresion de encoding**
- `admin.html` y `screen.html` mostraron mojibake (`Ã¡`, `Ã±`, `Â·`, emojis rotos) despues de una serie de ediciones con herramientas distintas sobre archivos HTML grandes
- La causa fue una mezcla de reescrituras con encoding inconsistente sobre archivos que ya tenian acentos, simbolos y emojis

**Correccion aplicada**
- `admin.html`: se dejo el fix de auth y se corrigio la regresion visual del panel
- `screen.html`: se restauro a la ultima version sana previa a la regresion de encoding
- Se publico el arreglo en `main` con commits `42c3f38` y `472c00c`

**Nota para trabajo compartido (Codex / Claude / otros)**
- Mantener estos HTML en UTF-8 y evitar conversiones automaticas de encoding
- Si se hace una restauracion puntual, comparar siempre contra un commit sano antes de reescribir archivos grandes
- En archivos con mucho texto visible, preferir cambios acotados sobre bloques especificos en vez de reserializar el archivo completo

---

### 2026-03-18 - Sesion 6

**Seguridad del panel admin**
- Eliminado el PIN maestro por defecto hardcodeado (`1234`)
- `admin.html`: el PIN maestro ahora se consulta desde Supabase al iniciar sesion y al cambiarlo
- `admin.html`: se dejo de confiar en `sessionStorage.ew_unlocked` para reabrir el panel tras recargar
- La validacion temporal del PIN maestro queda solo en memoria de sesion (`ew_master_pin_verified`)

**Render seguro en pantalla y admin**
- `screen.html`: mensajes del strip y waiting screen dejaron de renderizar contenido de invitados con `innerHTML`
- `screen.html`: la animacion `wave` ahora construye spans con `textContent` en lugar de interpolar HTML
- `screen.html`: mosaicos y polaroids ahora crean nodos DOM seguros y sanitizan URLs antes de asignarlas a `img.src`
- `admin.html`: la lista de contenido escapa `author`, `content` e IDs antes de renderizarlos en cards

**Notas**
- No se modifico la logica de moderacion automatica/manual
- Sigue pendiente endurecer seguridad real del lado servidor con RLS o backend, porque el proyecto sigue siendo frontend estatico con publishable key

---

### 2026-03-16 â€” SesiÃ³n 1

**Reacciones en fotos**
- Nueva tabla `reactions` en Supabase con `UNIQUE(post_id, guest_name)`
- guest.html: tab "GalerÃ­a" con todas las fotos del evento + botones â¤ï¸ðŸŽ‰ðŸ˜ðŸ”¥
- Una reacciÃ³n por foto por persona â€” cambiar emoji reemplaza el anterior
- screen.html: pills de reacciones en foto featured, actualizadas cada 5s, fade suave entre fotos

**Landing page (index.html)**
- Testimonios rediseÃ±ados: featured quote + 2 cards estÃ¡ticas (Swiper eliminado)
- Removido: secciÃ³n galerÃ­a, hero mockup desktop, botÃ³n "Ver demo en vivo", wa-float duplicado
- Limpieza: Swiper CDN, CSS huÃ©rfano, doble `const nav`, sp-wrap duplicado
- FAQ schema sincronizado con HTML

**screen.html**
- Fix carrusel: `featuredIdx` se recalcula por ID al llegar foto nueva
- Reacciones con fade in/out entre cambios de foto, sin animaciÃ³n en polls periÃ³dicos

**admin.html**
- URL de pantalla ya no desborda el card (`word-break:break-all`)

**guest.html**
- Tab "GalerÃ­a" con sistema de reacciones completo
- Tab "Votar" permanentemente oculto (votaciÃ³n aparece automÃ¡tica desde admin)
- Tabs: fade gradient derecha + peek animation para indicar scroll horizontal

---

### 2026-03-16 â€” SesiÃ³n 2

- Sonido por defecto cambiado a `none` en screen.html
- "Mis fotos": badge de reacciones por emoji con conteos reales (â¤ï¸2 ðŸŽ‰1 ðŸ”¥3)
- screen.html: fix fade reacciones entre fotos (sin `setTimeout` que borraba el contenido)

---

### 2026-03-16 â€” SesiÃ³n 3

**admin.html â€” Tab âš™ï¸ Funciones (Vista invitado)**
- CSS agregado para `.opt-toggle` / `.opt-track` / `.opt-thumb` (switches rosados/grises animados)
- `onclick` movido al `<label>` para que toda la fila sea clickeable
- Nuevos toggles: â¤ï¸ Reacciones en fotos (`showReactions`), ðŸŽ¨ PersonalizaciÃ³n de foto (`showPhotoEdit`)
- `GD_DEFAULTS`, `saveGuestDesign`, `showGuestDesign` actualizados
- Tarjetas de eventos: badge rosa `ðŸ”— custom_code` si tiene cÃ³digo personalizado, gris con primeros 8 chars del UUID si no

**guest.html**
- `gdFlags = {showReactions, showPhotoEdit}` actualizado por `applyGuestDesign`
- Selector corregido: `.gallery-reactions` (era `.rxn-btns`)
- Pickers (frame/filter/sticker) solo se muestran si `gdFlags.showPhotoEdit === true`
- Cards de galerÃ­a sin `.gallery-reactions` si `gdFlags.showReactions === false`

**index.html**
- Card de feature "âš™ï¸ Control total de funciones" en secciÃ³n Funcionalidades
- "âœ“ Control de funciones por evento" en pricing checklist

---

### 2026-03-16 â€” SesiÃ³n 4

**admin.html**
- Nuevo toggle `ðŸ—‘ Borrar fotos propias` (`showDeletePhoto`) en âš™ï¸ Funciones
- Fix card "CÃ³digo del evento": `flex-wrap`, font `clamp(28px,5vw,52px)`, botÃ³n `white-space:nowrap`, URL `overflow-wrap:anywhere`, `min-width:0` en contenedor flex

**guest.html**
- `gdFlags.showDeletePhoto` actualizado por `applyGuestDesign`
- BotÃ³n "ðŸ—‘ Eliminar" en "Mis fotos" solo se renderiza si `showDeletePhoto === true`

**screen.html**
- Eliminada llamada `playSound(cfg.sound)` del handler de nuevo post â€” pantalla ya no hace ruido

---

### 2026-03-16 â€” SesiÃ³n 5

**Marca de agua (watermark)**

*admin.html:*
- SecciÃ³n "Marca de agua" en tab Estilo: file input (PNG/SVG/WebP), posiciÃ³n (tl/tr/bl/br/center), tamaÃ±o (5â€“50%), opacidad (10â€“100%)
- `uploadWatermark(input)` â€” sube a `watermarks/{eventId}/wm.{ext}` en bucket `eventwall`
- `removeWatermark()` â€” limpia URL y oculta preview
- `saveGuestDesign` / `showGuestDesign` incluyen `wmUrl`, `wmPos`, `wmSize`, `wmOpacity`
- Fix: `BUCKET` no estÃ¡ definido en admin.html â†’ reemplazado con literal `'eventwall'`

*guest.html:*
- `gdFlags` extendido con `wmUrl`, `wmPos`, `wmSize`, `wmOpacity`
- `_wmImage` â€” `Image()` cacheada con `crossOrigin='anonymous'`; no recarga si URL no cambiÃ³
- `img.onload` re-renderiza el canvas si ya hay foto seleccionada
- Watermark dibujada al final de `renderPreviewCanvas()` con `ctx.globalAlpha` + `ctx.drawImage`
- `sendPhoto()` llama `renderPreviewCanvas()` antes de `canvas.toBlob()` para garantizar que la marca estÃ© quemada en el JPEG

*screen.html:*
- `<img id="screen-wm">` overlay absoluto sobre `#featured-img` (z-index:5, pointer-events:none)
- `applyScreenWatermark(gd)` â€” posiciona y opacifica el overlay segÃºn config
- `init()` carga `guest_design` y llama `applyScreenWatermark`

**Plantillas de pantalla (5 nuevas)**
- `TEMPLATES` + `applyTemplate` en admin.html: `xv` (XV AÃ±os), `corporate` (Corporativo), `birthday` (CumpleaÃ±os), `boho` (Boho), `sunset` (Sunset)

**Plantillas de diseÃ±o invitado (10 presets)**
- Tab "ðŸŽ¨ Plantillas" (primero) en config de Vista invitado, 10 cards con mini hero preview
- `applyGDTemplate(name)` â€” aplica colores + fonts por preset

**"QuiÃ©n reaccionÃ³" popover**
- guest.html: toque largo (500ms) o click derecho en botÃ³n de reacciÃ³n â†’ popover con nombres
- `showRxnPopover(e, btn, emoji)` â€” singleton div, posicionado con `getBoundingClientRect()`
- `rxnMap` restructurado: `{count, names:[]}` por emoji por post
- `renderGalleryCard` pasa `data-rxn-names` (JSON) en cada botÃ³n

**Fechas en formato DD/MM/AAAA**
- `formatDateES(str)` â€” convierte `YYYY-MM-DD` â†’ `DD/MM/AAAA`
- Aplicado en `ev-sub` de guest.html y screen.html

**index.html â€” Formulario de contacto**
- Campo fecha: `type="text"` con `maskDate(el)` (inserta `/` automÃ¡tico en pos 2 y 5)
- Labels: sin uppercase/letter-spacing, `font-size:13px`, emojis (ðŸ‘¤ðŸŽ‰ðŸ“…ðŸ‘¥ðŸ’¬)
- "Cantidad estimada de invitados" â†’ "Cantidad de invitados"

**Carrusel â€” nueva foto va al frente de la cola**
- Foto nueva se inserta en `photoPosts` justo despuÃ©s de la foto actual (`splice(insertAt, 0, p)`)
- En la prÃ³xima rotaciÃ³n, la foto nueva es la primera en aparecer
- Si no hay fotos todavÃ­a, aparece de inmediato

---

### Sesiones anteriores (resumen)

- PDF adjunto al email del Ã¡lbum (Edge Function con pdf-lib en Deno)
- AOS.js animaciones scroll en landing, marquee infinito proof bar
- Announcement bar, mobile menu fix, countdown dinÃ¡mico, nav active en index
- ModeraciÃ³n integrada en panel Contenido del admin
- Sidebar configurable en screen (ancho, visibilidad)
- EliminaciÃ³n instantÃ¡nea de mensajes/deseos en screen al moderar desde admin

---

### 2026-03-18 â€” SesiÃ³n 11

**Favicon y Ã­conos de pestaÃ±a**

*Assets:*
- Nuevo `favicon.ico` para la pestaÃ±a del navegador
- Nuevos `favicon-192.png` y `apple-touch-icon.png` para navegadores y accesos directos

*HTML:*
- `index.html`, `admin.html`, `guest.html` y `screen.html` ahora referencian el favicon y el icono touch

---

### 2026-03-18 â€” SesiÃ³n 12

**guest.html â€” UX mÃ¡s premium**

- La selecciÃ³n de foto ahora muestra una tarjeta de estado con nombre de archivo, peso y validaciÃ³n visual antes de enviar
- El `upload-zone` tiene mejor feedback visual al hover y al quedar una foto lista
- El overlay de envÃ­o pasÃ³ a una tarjeta mÃ¡s cuidada, con tÃ­tulo y descripciÃ³n segÃºn el tipo de contenido
- La pantalla de Ã©xito ahora cambia el mensaje y CTA segÃºn si se enviÃ³ foto, mensaje, audio o dedicatoria
- Los errores tÃ©cnicos se convierten en mensajes mÃ¡s claros para el invitado
- Los errores visibles ahora hacen scroll suave hasta el bloque correspondiente

---

### 2026-03-18 â€” SesiÃ³n 13

**screen.html â€” Robustez + branding + transiciones**

- Nuevo badge de conexiÃ³n para mostrar pantalla conectada, seÃ±al inestable o reconexiÃ³n
- `api()` ahora detecta timeouts/lentitud y actualiza el estado visual de conexiÃ³n
- Polling protegido con guards para evitar requests solapados cuando Supabase tarda
- `showFeatured()` ahora serializa transiciones para evitar parpadeos cuando llegan fotos seguidas
- Featured con entrada mÃ¡s cinematogrÃ¡fica y branding mÃ¡s consistente con glow/acento rosa
- Overlay de wishes mÃ¡s emocional, con entrada escalonada de autor/texto y fondo mÃ¡s rico

### 2026-03-18 â€” SesiÃ³n 14

**screen.html â€” no repetir contenido al refrescar**

- Mensajes, wishes y audios vistos ahora se guardan por evento sin depender de una key diaria
- Los “momentos” tambiÃ©n guardan el Ãºltimo ID mostrado en `localStorage`
- Al refrescar la pantalla, el contenido ya mostrado no vuelve a dispararse completo

### 2026-03-18 â€” SesiÃ³n 15

**admin.html + screen.html â€” diseÃ±os compartidos y configuraciones consistentes**

- El diseÃ±o de pantalla dejÃ³ de depender solo del `localStorage` del navegador del admin y ahora se guarda en `event_settings.screen_design`
- `screen.html` ahora prioriza `event_settings.screen_design` para aplicar el tema del evento y solo usa `localStorage` como fallback de compatibilidad
- La marca de agua de pantalla ahora se hidrata desde `event_settings.guest_design`, igual que el resto del flujo de invitado
- Los resets de diseÃ±o invitado y diseÃ±o de pantalla ahora limpian la configuraciÃ³n compartida del evento, no solo estado local del navegador

