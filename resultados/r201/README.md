# Tanque tipo R-201: patrón de flujo (exploratorio)

Caso `CASO_R201` de `src/setup.cpp`, corrido el 2026-10-01 en una RTX 3050 Ti Laptop. Los gráficos salen de `herramientas/graficar_r201.py`.

## Qué es y qué no es

Es un patrón de flujo **cualitativo**, construido con supuestos. En el proyecto, la geometría del R-201 está abierta: H/D, impulsor, diámetro, rpm y deflectores (DEC-OE2-004). Lo único definido es un volumen útil del orden de 5 m³, y aquí no se usa porque los resultados son adimensionales.

**Supuestos:**

| Elemento | Supuesto |
|---|---|
| Tanque | Estándar: H = T, D = T/3, C = T/3 |
| Deflectores | 4, de 0,1T, a 45°, 135°, 225° y 315°. El proyecto no menciona deflectores. |
| Impulsor | Turbina de 4 palas a 45°, ancho de pala 0,2D, bombeo descendente. Las palas inclinadas de 30–45° son candidatas del proyecto, sin selección. |
| Medio | Líquido newtoniano monofásico. El medio real es una suspensión de flakes de PET con reología desconocida. |
| Parte superior | Tapa no deslizante. El reactor real tiene superficie libre. |
| Régimen | Turbulento a Re = 29 000. El reactor real operaría a Re mayor. |

**Parámetros numéricos:**
- D = 60 celdas (T = 180).
- LES Smagorinsky, D3Q19 SRT en FP32.
- Re-voxelización del impulsor en cada paso.
- 10 revoluciones de arranque y 20 promediadas, con 8 instantáneas por revolución.

**Lo que no se reporta y por qué:**
- **Número de potencia:** con este método no valida (ver `validacion/rushton.md`).
- **rpm y potencia:** el proyecto no los fija.
- **Velocidades:** van relativas a la velocidad de punta de pala.

## Lo que muestran los gráficos

- **`r201_plano.png`**, plano vertical por el eje, a medio camino entre deflectores:
  - el chorro de las palas baja en diagonal hacia la esquina entre fondo y pared, sube por la pared hasta z/H ≈ 0,5 y vuelve al impulsor, que es el lazo típico de una turbina de palas inclinadas con bombeo descendente;
  - por encima de z/H ≈ 0,5 la circulación es más débil y desordenada;
  - las dos mitades del plano no son iguales, aunque deberían serlo por simetría. Indica que 20 revoluciones de promedio no alcanzan para un campo medio liso.
- **`r201_fondo.png`**, primera capa de fluido sobre el fondo:
  - la velocidad horizontal media llega a ≈ 0,08 veces la de punta;
  - es mínima en el centro, bajo el impulsor, en un anillo pegado a la pared y junto a los deflectores;
  - esas zonas son candidatas a acumular sólidos. Confirmarlo exige un modelo de sólidos en suspensión, que FluidX3D no tiene.

Ninguna de estas observaciones es un dato de proceso del R-201. Sirven para orientar preguntas de diseño (posición del impulsor, deflectores, zonas a instrumentar o muestrear), no para responderlas.
