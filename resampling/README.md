Fiber Resampling
======================
## Datos de ejemplo
En el siguiente enlace hay un sujeto de la base de datos ARCHI, con sus fibras originales (sobre-muestreadas y con cantidad variable de puntos).
https://drive.google.com/drive/folders/1-qYE4iCXVQHoxkwSgcqW1V2ExnsSvk4D?usp=sharing

## Ejemplo de uso

En primer lugar compilar el código:
```
gcc BundleTools_sp.c resampling.c -o resampling -lm
```
Ejecutar:
```
./resampling fileInput.bundles fileOutput.bundles points_per_fiber
```
## Parámetros de entrada
- **fileInput**: Archivo de tractografía de entrada en formato .bundles
- **fileOutput**: Archivo de tractografía remuestreada de salida, en formato .bundles y .bundlesdata
- **points_per_fiber**: Número de puntos por fibra a utilizar en el remuestreo

Nota: A pesar de que la llamada al código sólo pida el archivo .bundles, el archivo .bundlesdata correspondiente debe estar presente en la misma carpeta que el archivo .bundles.

Authors:
Narciso López López
Andrea Vázquez Varela
Last update: 27-01-2020
