# Guion Caja Negra — Etapa 2 (AGCL Gateway v1.6.4)

**Paquete público de verificación externa.**  
No modificar ni redistribuir el núcleo congelado (etapa-1). El código fuente real no forma parte de este repositorio.

---

## Preparación

```bash
export SDOS_BASE="http://127.0.0.1:8000"   # o la URL de la instancia autorizada
# Opcional:
# export CURL_INSECURE=1
# export BURST_N=80
# export OUT=evidence/phase_x.json
```

---

## FASE A — Edge / ráfaga

```bash
bash blackbox/scripts/phase_a_edge_burst.sh
```

Objetivo: observar comportamiento de `/health` y `/ready` bajo ráfaga.  
Con edge nginx de referencia se espera posible 429. Contra el Gateway directo no debe aparecer 429 de proceso en estas rutas públicas.

---

## FASE B — Autenticación fail-closed

```bash
python3 blackbox/scripts/phase_b_auth_failclosed.py
```

Casos:
- Sin headers de autenticación
- API Key incorrecta
- Firma inválida

Resultado esperado: 401 o 403 en todos los casos.

---

## FASE C — Integridad (ancla)

```bash
export SDOS_LEDGER_ANCHOR_PATH="/ruta/al/ancla/de/la/instancia"
python3 blackbox/scripts/phase_c_integrity_probe.py
```

Objetivo: comprobar que el sistema detecta manipulación del ancla (respuesta 503 en `/ready` tras corrupción controlada).  
**Solo ejecutar en entornos de laboratorio autorizados.**

---

## Resultados

Guardar salidas en la carpeta `evidence/` de este repositorio.
