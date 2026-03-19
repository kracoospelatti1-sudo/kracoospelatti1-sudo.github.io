---
name: EventWall project context
description: Stack, file structure, auth model, custom_code feature, album email logic, and admin panel structure
type: project
---

EventWall is a photo/message wall app for events displayed on a TV screen. Guests upload photos and messages via a guest URL; the host manages everything via admin.html.

**Stack:** Vanilla HTML/CSS/JS, Supabase backend, GitHub Pages hosting.

**Key files:**
- admin.html — full admin panel (single file, ~74k tokens)
- guest.html — guest upload interface
- index.html — landing/pricing page

**Auth model:** PIN-based. Master PIN for admin, per-event client PIN with configurable duration (no vencimiento to 72h).

**Custom code feature:** Events can have a slug (e.g. "boda-caro-pablo") used in URLs instead of the UUID.

**Album email logic:** When an event is deleted, the full album (photos + messages + wishes) is automatically emailed to the client's stored email address.

**Admin panel structure (current):**
- Left sidebar (240px): logo, nav buttons, footer with logout
- Main area: full-width page content
- Grid: `grid-template-columns: 240px 1fr`

**Nav sections in sidebar:**
- Global: Eventos, Nuevo evento
- Per-event (shown after selecting): Dashboard (Inicio rápido), Links & QR, Diseño, Álbum, Contenido (messages moderation)
- Tools: Modo impresión, Votaciones, Vista invitado, Momentos, Configuración, Ayuda

**Design system:**
- Dark theme: --bg:#07070b, --surface:#111116, --surface2:#1a1a22, --border:#24242f
- Accent: --pink:#f0176f (with glow/dim variants)
- Gold: #f5a623 (secondary accent)
- Fonts: Syne (headings, 800w), DM Sans (body)
- Border radius: 10-16px cards, 12px inputs
- Active nav: pink-dim bg + left border 2px pink

**Key UX patterns already in place:**
- Skeleton loaders on content
- Custom confirm modals (not browser default)
- Toast notifications (bottom-right)
- Auto-approve toggle for moderation
- Design editor: template grid + advanced accordion with sub-tabs (Colores, Tipografía, Layout, Burbuja...)
- Guest design page has phone preview sidebar
- Mobile: sidebar becomes fixed drawer with hamburger
