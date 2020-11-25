# Table of contents
1. [Fiber-Mesh Intersection (Modified)](#intersection)
2. [Some paragraph](#bundle_classification)
3. [Another paragraph](#intersection_classification)

## Fiber-Mesh Intersection (Modified) <a name="intersection"></a>
Este algoritmo es una modificación de aquel utilizado en [1]. Específicamente, esta versión evalúa la intersección con un hemisferio a la vez, en lugar de ambos al mismo tiempo; además, esta versión también considera el cálculo de los perfiles de conectividad, por lo que no descarta las fibras que intersectan con la corteza en sólo uno de sus extremos (a diferencia del original, que sólo considera aquellas que conectan en ambas extremidades). Para más detalles, leer el extracto de MT incluido en la carpeta.

### Ejemplo de uso
Ejecutar (desde la terminal o desde el código fuente, por ejemplo en spyder):
```
python3 interx.py
```
A diferencia de los algoritmos de preprocesamiento, este código no cuenta con parámetros modificables desde terminal. Por lo tanto, las rutas de los mallados corticales y de los clusters deben ser modificadas directamente en el archivo interx.py.

Por defecto, el algoritmo se ejecuta 79 veces, correspondiente a los 79 sujetos de la base de datos ARCHI. Esto también se puede modificar en el código interx.py

### Archivos de entrada
- Mallados corticales en formato .obj, un archivo por cada hemisferio.
- Fascículos/clusters en formato .bundles y .bundlesdata, resampleados a 21 puntos por fibra, y separados en un archivo por cada fascículo/cluster.

### Archivos de salida
- Carpeta "/intersection/", que contiene los datos de intersección de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.intersectiondata), los cuales son:

  - Índice del triángulo que intersecta con el extremo inicial de la fibra.
  - Índice del triángulo que intersecta con el extremo final de la fibra.
  - Punto exacto de intersección con el extremo inicial de la fibra.
  - Punto exacto de intersección con el extremo final de la fibra.
  - Índice de la fibra que intersecta con los triángulos.

- Carpeta "/membership/", que contiene los datos de conectividad/pertenencia de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.membershipdata). Los valores posibles son:

  - (1,1): Cluster intersecta en ambos extremos.
  - (1,0): Cluster sólo intersecta en su extremo inicial.
  - (0,0): Cluster no intersecta.

## Bundle Classification <a name="bundle_classification"></a>
Este algoritmo es una modificación de aquel utilizado en [1]. Específicamente, esta versión evalúa la intersección con un hemisferio a la vez, en lugar de ambos al mismo tiempo; además, esta versión también considera el cálculo de los perfiles de conectividad, por lo que no descarta las fibras que intersectan con la corteza en sólo uno de sus extremos (a diferencia del original, que sólo considera aquellas que conectan en ambas extremidades). Para más detalles, leer el extracto de MT incluido en la carpeta.

### Ejemplo de uso
Ejecutar (desde la terminal o desde el código fuente, por ejemplo en spyder):
```
python3 interx.py
```
A diferencia de los algoritmos de preprocesamiento, este código no cuenta con parámetros modificables desde terminal. Por lo tanto, las rutas de los mallados corticales y de los clusters deben ser modificadas directamente en el archivo interx.py.

Por defecto, el algoritmo se ejecuta 79 veces, correspondiente a los 79 sujetos de la base de datos ARCHI. Esto también se puede modificar en el código interx.py

### Archivos de entrada
- Mallados corticales en formato .obj, un archivo por cada hemisferio.
- Fascículos/clusters en formato .bundles y .bundlesdata, resampleados a 21 puntos por fibra, y separados en un archivo por cada fascículo/cluster.

### Archivos de salida
- Carpeta "/intersection/", que contiene los datos de intersección de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.intersectiondata), los cuales son:

  - Índice del triángulo que intersecta con el extremo inicial de la fibra.
  - Índice del triángulo que intersecta con el extremo final de la fibra.
  - Punto exacto de intersección con el extremo inicial de la fibra.
  - Punto exacto de intersección con el extremo final de la fibra.
  - Índice de la fibra que intersecta con los triángulos.

- Carpeta "/membership/", que contiene los datos de conectividad/pertenencia de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.membershipdata). Los valores posibles son:

  - (1,1): Cluster intersecta en ambos extremos.
  - (1,0): Cluster sólo intersecta en su extremo inicial.
  - (0,0): Cluster no intersecta.

## Intersection Classification <a name="intersection_classification"></a>
Este algoritmo es una modificación de aquel utilizado en [1]. Específicamente, esta versión evalúa la intersección con un hemisferio a la vez, en lugar de ambos al mismo tiempo; además, esta versión también considera el cálculo de los perfiles de conectividad, por lo que no descarta las fibras que intersectan con la corteza en sólo uno de sus extremos (a diferencia del original, que sólo considera aquellas que conectan en ambas extremidades). Para más detalles, leer el extracto de MT incluido en la carpeta.

### Ejemplo de uso
Ejecutar (desde la terminal o desde el código fuente, por ejemplo en spyder):
```
python3 interx.py
```
A diferencia de los algoritmos de preprocesamiento, este código no cuenta con parámetros modificables desde terminal. Por lo tanto, las rutas de los mallados corticales y de los clusters deben ser modificadas directamente en el archivo interx.py.

Por defecto, el algoritmo se ejecuta 79 veces, correspondiente a los 79 sujetos de la base de datos ARCHI. Esto también se puede modificar en el código interx.py

### Archivos de entrada
- Mallados corticales en formato .obj, un archivo por cada hemisferio.
- Fascículos/clusters en formato .bundles y .bundlesdata, resampleados a 21 puntos por fibra, y separados en un archivo por cada fascículo/cluster.

### Archivos de salida
- Carpeta "/intersection/", que contiene los datos de intersección de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.intersectiondata), los cuales son:

  - Índice del triángulo que intersecta con el extremo inicial de la fibra.
  - Índice del triángulo que intersecta con el extremo final de la fibra.
  - Punto exacto de intersección con el extremo inicial de la fibra.
  - Punto exacto de intersección con el extremo final de la fibra.
  - Índice de la fibra que intersecta con los triángulos.

- Carpeta "/membership/", que contiene los datos de conectividad/pertenencia de cada fascículo en cada caso (L_hemi_direct, R_hemi_direct, L_hemi_inverse, R_hemi_inverse), almacenados en archivos binarios (.membershipdata). Los valores posibles son:

  - (1,1): Cluster intersecta en ambos extremos.
  - (1,0): Cluster sólo intersecta en su extremo inicial.
  - (0,0): Cluster no intersecta.


## Referencias
<a id="1">[1]</a>
F. Silva, M. Guevara, C. Poupon, J.-F. Mangin, C. Hernandez, and P. Guevara, “Cortical Surface Parcellation Based on Graph Representation of Short Fiber Bundle Connections,” in 2019 IEEE 16th International Symposium on Biomedical Imaging (ISBI 2019), 2019.
