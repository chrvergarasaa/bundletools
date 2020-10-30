FFClust
======================
## Dependencias de Código
Para utilizar el código, es necesario instalar las siguientes librerías:
- Numpy: https://numpy.org/
- Sklearn: https://scikit-learn.org/stable/
- Scipy: https://www.scipy.org/
- Networkx: https://networkx.github.io/

### OPCIÓN 1: Instalación de dependencias via pip3 en Ubuntu
```
pip3 install numpy
pip3 install scikit-learn
pip3 install scipy
pip3 install networkx
```

### OPCIÓN 2: Instalación de dependencias via apt en Ubuntu
```
sudo apt install python3-numpy
sudo apt-get install python3-sklearn
sudo apt install python3-scipy
sudo apt-get install python3-networkx
```

## Datos de ejemplo
En el siguiente enlace hay un sujeto de la base de datos ARCHI, con sus fibras remuestreadas a 21 puntos por fibra.
https://drive.google.com/drive/folders/1-qYE4iCXVQHoxkwSgcqW1V2ExnsSvk4D?usp=sharing

## Ejemplo de uso

Si es necesario, compilar antes el código de segmentación en segmentation_clust_v1.2/
```
gcc -fPIC -shared  -O3 -o segmentation.so segmentation.c -fopenmp -ffast-math
```
Ejecución del algoritmo FFClust:
```
python3 main.py --infile example_data/example_sub_resampled.bundles --outdir result
```
## Parámetros de entrada
- **--points**: Puntos a utilizar en el clustering inicial de mapeo (Minibatch K-Means) **Por defecto: 0,3,10,17,20**
- **--ks**: Número de clusters a utilizar por cada punto en K-means para el mapeo **Por defecto: 300, 200, 200, 200, 300**
- **--thr-seg**: Umbral mínimo para la segmentación en mm (en el paper: dRMax) **Por defecto: 6**
- **--thr-join**: Umbral mínimo para la unión/fusión en mm (en el paper: dMMax) **Por defecto: 6**
- **--infile**: Archivo de tractografía de entrada (las fibras deben estar remuestreadas a 21 puntos por fibra) en formato .bundles y .bundlesdata
- **--outdir**: Directorio para guardar los archivos de salida

## Formato de datos de entrada/salida
### Archivos de entrada
Se dispone de un sujeto de prueba en https://drive.google.com/drive/folders/1-qYE4iCXVQHoxkwSgcqW1V2ExnsSvk4D?usp=sharing.
- example_sub_resampled.bundles y example_sub_resampled.bundlesdata: Corresponde a un sujeto de la base de datos ARCHI, cuyas fibras han sido remuestreadas a 21 puntos equidistantes.

### Archivos de salida
- finalClusters.bundles/.bundlesdata: Esta carpeta contiene todos los clusters resultantes juntos, en formato .bundles/.bundlesdata.
- finalClusters.hie: Jerarquía AIMS con etiquetas y colores de cada cluster (para visualización, por ejemplo en Anatomist).
- centroids.bundles/.bundlesdata: Este archivo contiene todos los centroides ordenados de los clusters. Por ejemplo, el cluster 0.bundles/.bundlesdata corresponde al centroide que está en posición 0 en centroids.bundles/bundlesdata.
- centroids.hie: Jerarquía AIMS con etiquetas y colores de cada centroide.
- stats.log: Este archivo contiene el tiempo de ejecución y el número de clusters en cada etapa del algoritmo.

## Referencias
<a id="1">[1]</a> 
A. Vázquez, N. López-López, A. Sánchez, J. Houenou, C. Poupon, J.-F. Mangin, C. Hernández, and P. Guevara, “FFClust: Fast fiber clustering for large tractography datasets for a detailed study of brain connectivity,” NeuroImage, vol. 220, p. 117070, Oct. 2020.
