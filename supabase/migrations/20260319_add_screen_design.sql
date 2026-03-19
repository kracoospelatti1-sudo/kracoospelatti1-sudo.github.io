alter table public.event_settings
add column if not exists screen_design jsonb;

comment on column public.event_settings.screen_design is
'Configuracion compartida de screen.html por evento';
