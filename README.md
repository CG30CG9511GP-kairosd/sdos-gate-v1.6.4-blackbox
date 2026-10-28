# AGCL Gateway v1.6.4 — Caja Negra Pública

**Paquete público de verificación externa (black-box)**  
Código fuente real del Gateway: **no incluido**.

| Nivel | Nombre | Descripción |
|-------|--------|-------------|
| **Empresa** | **SDOS** | Sierra Digital OS |
| **Metodología** | **AGCL** | Marco de control y gobernanza |
| **Producto** | **AGCL Gateway** | Primer servicio de la plataforma |

Este repositorio permite verificar los **controles de seguridad observables** del AGCL Gateway v1.6.4 sin exponer la implementación interna.

> Evidencia de laboratorio ≠ aprobación de producción.

---

## Simulador interactivo (demo de campaña)

**Frase:** *El agente propone. El humano autoriza.*

Archivo: [`demo/index.html`](demo/index.html)

- Es una **simulación educativa** (no es el API ni el binario real).
- Para LinkedIn / navegador: activa **GitHub Pages** en este repo (`Settings → Pages → Deploy from branch main`) y usa:
  - `https://cg30cg9511gp-kairosd.github.io/sdos-gate-v1.6.4-blackbox/demo/`
- Vista previa rápida (sin Pages):
  - [htmlpreview del simulador](https://htmlpreview.github.io/?https://github.com/CG30CG9511GP-kairosd/sdos-gate-v1.6.4-blackbox/blob/main/demo/index.html)

---

## Qué contiene este repositorio

| Contenido | Descripción |
|-----------|-------------|
| `demo/` | Simulador HTML AGCL Gateway (campaña) |
| `FREEZE/` | Hashes SHA-256 del núcleo congelado + estado de la etapa |
| `blackbox/` | Scripts de prueba externa (Fases A, B, C) + guion |
| `deploy/` | Configuración de referencia edge (nginx) + compose de ejemplo (sin secretos) |
| `docs/` | Documentación de controles observables |
| `evidence/` | Espacio para resultados de campañas de verificación |

**No contiene**:
- Código fuente de `app/` (main, request_auth, ledger, authz, etc.)
- Claves, secretos ni configuraciones reales
- Implementación interna del ledger, anclas o criptografía

---

## Controles verificables desde fuera (contrato público)

| Control | Verificación externa |
|---------|----------------------|
| Versión 1.6.4 | Endpoint `/health` o `/ready` |
| Autenticación Ed25519 + API Key | Scripts Fase B |
| Anti-replay (nonce + ventana ±5 min) | Replay de nonce real → 401 |
| Deny-by-default de rutas | Rutas no registradas → 401 |
| Límite de cuerpo 1 MiB | Body > 1 MiB → 413 |
| Rate limit edge 30 r/s | Config nginx + respuesta 429 |
| Single-worker | Configuración de despliegue de referencia |
| Ledger + ancla en volúmenes separados | `docker-compose.prod.yml` de referencia |

---

## Integridad del núcleo (FREEZE)

Los siguientes hashes corresponden al código fuente real congelado el **2026-10-26T23:54:06Z**:

```
ed31dafbd74bebfb0773ab0bbbd05d917d17b0eb35cfa5a372b063a3207bc724  app/main.py
a17abf6b513b131f21081d244172600fb582eb41d6e81eb0f879eb93d07b7f15  app/ledger.py
e89245246610ad69868ef38b70094defc24dda4f0d8859531215113924f57e3a  app/ledger_anchor.py
8ca897982cbfa54a9366dcc9269e83f1644600937c06660e86c8484edbb60de8  app/request_auth.py
bdd4f098ce89c33777a736b0249f9300c53bd8a00ad5d1cfaebf765c4999ee19  tests/conftest.py
```

**Estado declarado**:  
`AGCL Gateway v1.6.4 ETAPA 1 CONGELADA — 124 passed / 20 skipped. Controles no rediseñados.`

---

## Cómo ejecutar las pruebas de caja negra

```bash
export SDOS_BASE="http://127.0.0.1:8000"

# FASE A — Edge / ráfaga
bash blackbox/scripts/phase_a_edge_burst.sh

# FASE B — Fallo cerrado de autenticación
python3 blackbox/scripts/phase_b_auth_failclosed.py

# FASE C — Integridad del ancla
python3 blackbox/scripts/phase_c_integrity_probe.py
```

Los resultados se pueden guardar en `evidence/`.

---

## Despliegue de referencia (solo configuración)

La carpeta `deploy/` contiene:
- `nginx/nginx.conf` — rate limit edge 30 r/s → 429
- `docker-compose.prod.yml` — volúmenes separados (ledger ≠ anchor) + single-worker
- `env.production.example` — plantilla sin valores reales

Estas configuraciones son de **referencia**. El código del servicio no se incluye.

---

## Autor

**SDOS** · Metodología **AGCL**  
Producto: **AGCL Gateway**

---

## Licencia y propiedad

Todo el código fuente del AGCL Gateway, diseños, algoritmos y documentación interna son **propiedad exclusiva** de sus titulares (SDOS).  
Este repositorio público solo distribuye material de verificación externa y configuraciones de referencia no secretas.

Uso no autorizado con fines de ingeniería inversa del sistema real está prohibido.
