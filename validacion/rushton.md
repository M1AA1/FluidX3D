# Validación Rushton: número de potencia

Caso `CASO_RUSHTON` de `src/setup.cpp`. Corridas del 2026-10-01 en una RTX 3050 Ti Laptop (4 GB), con FluidX3D v3.8 más los cambios de este fork.

## Configuración

- **Geometría estándar** (Hartmann et al. 2004): H = T, D = T/3, C = T/3, 4 deflectores de 0,1T a 0,017T de la pared, disco de 0,75D, 6 palas de 0,25D × 0,2D, tapa no deslizante.
- **Parámetros numéricos** (Derksen & Van den Akker 1999): D = 60 celdas (T = 180), Re = 29 000, punta de pala ≈ 0,1, LES Smagorinsky (`SUBGRID`), D3Q19 SRT en FP32.
- **Supuestos propios**, no del estándar:
  - espesor de palas y disco: max(2; 0,04D) = 2,4 celdas;
  - deflectores de 2 celdas;
  - radio del eje: 0,08D.
- **Duración:** 30 revoluciones, 1885 pasos por revolución; se descartan 10 de arranque y se promedian 20.

## Resultados

| Variante | Po por torque de reacción en paredes | Otras medidas |
|---|---|---|
| Re-voxelización cada 5 pasos | **2,17** (bloques de 5 rev: 2,12–2,19) | Po por disipación integrada: 0,90 (cota inferior) |
| Re-voxelización cada paso | **2,82** (bloques de 5 rev: 2,76–2,85) | — |
| Referencia experimental (Derksen & Van den Akker 1999, Re ≈ 30 000) | 4,6–5,9 | — |

**Veredicto: no valida.** Las dos variantes quedan bajo el rango.

## Observaciones

1. **El resultado depende del intervalo de re-voxelización.** Pasar de 5 pasos a 1 sube Po un 30 %. Es la dependencia que advierte el autor de FluidX3D en el issue #141.
2. **El torque sobre el impulsor no sirve.** Da −119 a −132, sin sentido físico. Las celdas interiores del impulsor llevan velocidad impuesta y `update_force_field` les asigna una fuerza 2ρu que sesga la suma. Por eso la medida principal es el torque de reacción sobre las paredes fijas.
3. **El voxelizador pierde una capa a lo largo del eje de giro.** Trunca a enteros las distancias de cruce (`(ushort)d` en `voxelize_mesh`). Efectos medidos:
   - palas: 2244 celdas de 2592 nominales (11 capas de alto en vez de 12);
   - disco: 1472 celdas, cuando deberían ser ≈ 2900 (1 capa en vez de 2).
4. **La disipación integrada es una cota inferior.** Da Po = 0,90 porque excluye las celdas vecinas a sólidos y usa diferencias finitas. Que quede bajo el torque de paredes es coherente: ambas medidas indican que el impulsor simulado transfiere poca potencia, no que el torque esté mal medido.
5. **El torque instantáneo oscila ±115–150 % alrededor de la media.** Es coherente con pulsos de presión generados en cada re-voxelización. Los promedios por bloques son estables.
6. **Las corridas son deterministas.** Repetir la variante de 5 pasos dio exactamente el mismo Po (2,167).
7. **Rendimiento.** Con cargador conectado, la variante de 5 pasos tarda unos 5 minutos y la de 1 paso unos 12. Con batería, la GPU baja a estado P5 y rinde unas 8 veces menos.

## Causas posibles aún no separadas

- La re-voxelización discreta borra fluido donde entra la pala y crea fluido en equilibrio donde sale, en vez de empujarlo. Eso puede reducir la presión frente a la pala.
- La pérdida de una capa de altura de las palas explica a lo sumo un ≈ 8 %.
- La resolución: palas de 2–3 celdas con paredes en escalera, a D = 60.
