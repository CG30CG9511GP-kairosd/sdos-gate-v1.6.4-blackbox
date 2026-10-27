# AGCL Gateway v1.6.4 — Caja Negra Pública (Etapa 2)

**Paquete público de verificación externa (black-box)**  
Código fuente real del Gateway: **no incluido**. Propiedad de Sierra Digital OS / AGCL.

Este repositorio permite auditar y verificar los **controles de seguridad observables** del **AGCL Gateway v1.6.4** sin exponer la implementación interna.

> Evidencia de laboratorio ≠ aprobación de producción.  
> Completar checklist de go-live antes de tráfico real.

---

## Qué contiene este repositorio

| Contenido | Descripción |
|-----------|-------------|
| `FREEZE/` | Hashes SHA-256 del núcleo congelado + estado de la etapa |
| `blackbox/` | Scripts de prueba externa (Fases A, B, C) + guion |
| `deploy/` | Configuración de referencia edge (nginx) + compose de ejemplo (sin secretos) |
| `docs/` | Documentación de controles y alcance |
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
| Autenticación Ed25519 + API Key | Scripts Fase B + vectores de ataque |
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

Ver archivos en `FREEZE/` para estado completo.

**Estado declarado**:  
`AGCL Gateway v1.6.4 ETAPA 1 CONGELADA — 124 passed / 20 skipped. Controles no rediseñados.`

---

## Cómo ejecutar las pruebas de caja negra

### Requisitos
- Instancia del AGCL Gateway accesible (proporcionada por el operador o entorno de laboratorio)
- `bash`, `python3`, `curl` (o equivalente)

### Variables de entorno mínimas
```bash
export SDOS_BASE="https://tu-instancia-o-localhost:8000"   # o http://127.0.0.1:8000
export SDOS_API_KEY="..."                                  # solo si la instancia lo requiere para algunos casos
```

### Guion oficial (Etapa 2)

Ver `blackbox/GUION_ETAPA2.md`.

```bash
# FASE A — Edge / ráfaga
bash blackbox/scripts/phase_a_edge_burst.sh

# FASE B — Fallo cerrado de autenticación
python3 blackbox/scripts/phase_b_auth_failclosed.py

# FASE C — Integridad (requiere rutas de ledger/ancla configuradas en la instancia)
python3 blackbox/scripts/phase_c_integrity_probe.py
```

Los resultados se pueden guardar en `evidence/`.

---

## Despliegue de referencia (solo configuración)

La carpeta `deploy/` contiene:
- `nginx/nginx.conf` — rate limit edge 30 r/s → 429, TLS, headers de seguridad
- `docker-compose.prod.yml` — patrón de volúmenes separados (ledger ≠ anchor) y single-worker
- `env.production.example` — plantilla de variables (sin valores reales)

Estas configuraciones son de **referencia**. El código del servicio AGCL Gateway no se incluye.

---

## Alcance y limitaciones

- Este repositorio es un **paquete de verificación externa**.
- No sustituye una auditoría de código fuente ni un dictamen de campaña firmado.
- Cualquier uso de los scripts contra instancias de producción requiere autorización explícita del operador.
- El código fuente real permanece privado y bajo control de Sierra Digital OS / AGCL.

---

## Autor / producto

**AGCL Gateway · Sierra Digital OS**  
Primer servicio de la plataforma.  
Metodología de congelación + verificación por caja negra.

---

## Licencia y propiedad

Todo el código fuente del AGCL Gateway, diseños, algoritmos y documentación interna son **propiedad exclusiva** de sus titulares.  
Este repositorio público solo distribuye material de verificación externa y configuraciones de referencia no secretas.

Uso no autorizado del material aquí presente con fines de ingeniería inversa del sistema real está prohibido.
