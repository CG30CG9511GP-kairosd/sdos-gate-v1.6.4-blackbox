# Campaña Etapa 2 — Caja Negra Pública

**Versión del Gate**: 1.6.4  
**Tipo de paquete**: Verificación externa (black-box)  
**Fecha de preparación del paquete público**: 2026-10-27  

## Objetivo de la campaña

Permitir la verificación independiente de los controles de seguridad **observables** del SDOS Gate v1.6.4 sin exponer el código fuente real ni secretos operativos.

## Contenido del paquete

- Hashes de integridad del núcleo congelado (`FREEZE/`)
- Scripts de prueba externa (Fases A, B, C)
- Configuración de referencia de edge y despliegue
- Documentación de controles observables
- Avisos de propiedad intelectual

## Qué queda fuera (privado)

- Todo el código fuente de la aplicación (`app/`)
- Claves, secretos y configuraciones reales
- Resultados de campañas internas previas que contengan datos sensibles

## Cómo usar este paquete

1. Clonar este repositorio.
2. Apuntar `SDOS_BASE` a una instancia autorizada del Gate.
3. Ejecutar el guion en `blackbox/GUION_ETAPA2.md`.
4. Depositar evidencias en `evidence/`.

## Estado

Paquete listo para publicación en GitHub (modo público o privado restringido).
