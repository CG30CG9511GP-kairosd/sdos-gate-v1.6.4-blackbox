# Controles Observables — AGCL Gateway v1.6.4

Documento de referencia para verificación externa (caja negra).

## 1. Autenticación y autorización

- Toda ruta protegida exige:
  - Header `X-SDOS-API-Key` válido (≥ 32 bytes)
  - Firma Ed25519 válida sobre representación canónica de la petición
  - Timestamp dentro de ventana ±300 segundos
  - Nonce único por tenant (anti-replay)
- Claims de privilegio presentes en el body (`role`, `authorized`, etc.) **no autorizan**.
- Rutas no registradas → 401 (deny-by-default).

## 2. Anti-replay

- Nonce de un solo uso, scoped por `tenant_id`.
- Ventana de reloj: 300 segundos (5 minutos).
- Replay de un nonce ya visto → 401.

## 3. Límites de recurso

- Cuerpo máximo: 1 MiB (1.048.576 bytes) → respuesta 413.
- Rate limit de edge (nginx de referencia): 30 peticiones/segundo → 429.
- Rate limit de proceso (complementario) existe en la implementación real.

## 4. Disponibilidad y despliegue de referencia

- Health: `GET /health` y `GET /ready` (públicos).
- Único worker de proceso recomendado (configuración de referencia).
- Ledger y ancla anti-rollback en volúmenes/almacenamiento separados.

## 5. Integridad

- Hashes SHA-256 del núcleo publicados en `FREEZE/SHA256_CORE.txt`.
- Cualquier discrepancia con el binario/imagen desplegada indica modificación no autorizada del núcleo congelado.
