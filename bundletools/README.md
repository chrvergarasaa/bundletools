BundleTools Base
======================
BundleTools es una librería/módulo de Python, desarrollada y escrita por la profesora Pamela Guevara y miembros antiguos/actuales del su grupo de trabajo. Esta contiene varias funciones utilizadas en el manejo de datos de tractografía obtenidos mediante dMRI, principalmente aquellas relacionadas con Input/Output. 

## Dependencias de Código
- Numpy: https://numpy.org/

## Versiones
En esta carpeta se encuentran dos versiones de la librería:

- **bundleTools.py:** Corresponde a la librería original, y es la más completa.
- **bundleTools3.py:** Es una versión modificada para su uso en Python 3. Sin embargo, las modificaciones son en realidad bastante sencillas, ya que sólo se refieren a la diferencia de sintaxis entre Python 2 y Python 3 (por ejemplo, la sintaxis de _print_). En todo caso, algunas funciones de bundleTools original también funcionan con Python3 (y viceversa), por lo que es recomendable cargar las dos librerías y ver cuál funciona en un determinado escenario.

## Funciones
A continuación se realiza una breve descripción de las funciones incluidas en la librería. Cabe destacar que sólo están incluidas las que yo he utilizado, ya que desconozco el funcionamiento de las demás; no obstante, el nombre de las funciones es bastante autoreferente.

- **getBundleNames:** Devuelve una lista con los nombres de los fascículos en los que se encuentran agrupadas las fibras. Esto es útil, por ejemplo, para fibras segmentadas. Si no existen grupos, la función devuelve una lista con un sólo elemento (usualmente el nombre por defecto 'points'). 

- **getBundleNamesAndSizes:** Devuelve una tupla, en donde el primer elemento es la misma lista devuelta por la función anterior, el segundo es una lista del mismo tamaño con la cantidad de fibras correspondiente a cada grupo, y el último elemento es la cantidad total de curvas contenidas en el archivo.

- **getBundleSize:** Obtiene la cantidad de curvas en un archivo .bundles.

- **getSymmetricBundle:** Recibe un archivo .bundles, obtiene una versión simétrica de las curvas, y las guarda en otro archivo .bundles. Esta función mantiene los grupos en caso de fibras segmentadas. La simetría se obtiene como el negativo de las coordenada x original, por lo que el resultado corresponde a una simetría lateral (respecto al plano sagital).

- **mesh_neighbors:** Recibe como entrada un conjunto de polígonos (por ejemplo, una mallado cortical), y devuelve una lista con largo igual a la cantidad de triángulos, donde cada elemento es una lista con los índices de los triángulos vecinos de ese triángulo particular, donde el vecindario se define según aristas y/o vértices en cómun.
Por ejemplo, si el elemento 425 de la lista es [14, 349, 500], eso quiere decir que los vecinos del triángulo 425 son los triángulos 14, 349 y 500.

- **read_bundle:** Lee un archivo .bundles, y entrega una lista de fibras, donde cada fibra es una lista de puntos con coordenadas en tres ejes ortogonales (x,y,z). En caso de leer un archivo con fibras agrupadas, esta función ignora los grupos y almacena todas las fibras dentro de una misma lista.

- **read_bundle_severalbundles:** Similar a la función anterior; sin embargo, esta respeta los grupos en el caso de fibras agrupadas. El resultado de esta función es una tupla, en donde el primer elemento es una lista de listas, cada una de ellas correspondientes a un distinto fascículo de fibras, mientras que el segundo elemento es una lista con el nombre de cada fascículo.

- **read_intersection:** Recibe como argumento un archivo .intersectiondata, y devuelve una tupla con la información de intersección entre un fascículo y mallado cortical. La tupla contiene 5 elementos (ver código Intersection):

  - Índice del triángulo que intersecta con el extremo inicial de la fibra.
  - Índice del triángulo que intersecta con el extremo final de la fibra.
  - Punto exacto de intersección con el extremo inicial de la fibra.
  - Punto exacto de intersección con el extremo final de la fibra.
  - Índice de la fibra que intersecta con los triángulos.

- **read_mesh:** Lee un archivo en formato .mesh, que contiene polígonos y vértices (que en nuestro caso se usa para almacenar mallados corticales). Devuelve una tupla, en donde el primer elemento es una lista de vértices, cada uno con su ubicación espacial en coordenadas (x,y,z). El segundo elemento es una lista de triángulos (polígonos), donde cada uno tiene una lista con los índices de los tres vértices que lo forman. Por ejemplo, si el elemento 424 contiene una lista [100,125,170], eso significa que el triángulo #424 está formado por los vértices 100, 125, y 170; luego, las coordenadas de cada uno de éstos vértices se puede buscar en el primer elemento de la tupla.

- **read_mesh_obj:** Esta función es casi idéntica la anterior; sin embargo, trabaja con archivos (mallados) en formato .obj. Además de esto, el funcionamiento es exactamente el mismo.

- **read_transformed_mesh_obj:** Esta función es idéntica a la anterior; sin embargo, está adaptado para leer el formato específico de los mallados .obj transformados al espacio Talairach (que por alguna razón es distinto al de los mallados .obj originales).

- **read_parcels:** Similar a **read_intersection**, esta función lee un archivo .parcelsdata, el que contiene información sobre una parcela obtenida por el código de parcellation, específicamente guarda una lista con los triángulos del mallado que corresponden a esa parcela en particular. 

- **write_bundle:** Función que exporta una lista de fibras a un archivo .bundles en disco. Las fibras deben tener el mismo formato que el resultante al leer un archivo con la función **read_bundle**; es decir, debe ser una lista (fibras) donde cada elemento es un arreglo Numpy (puntos), y cada elemento de estos es un arreglo de float32 (coordenadas x,y,z). La función creará tanto el archivo .bundles como el .bundlesdata correspondiente.

- **write_bundle_severalbundles:** Similar a la función anterior; sin embargo, esta se utiliza para guardar fibras segmentadas en distintos grupos. Para esto, las fibras deben estar agrupadas dentro de la lista maestra (es decir, mientras que en fibras no segmentadas la lista maestra contiene N elementos correspondientes a N fibras, en el caso de fibras segmentadas debe contener M elementos (listas) correspondientes a M grupos, y dentro de cada uno de ellos están las fibras de cada grupo). Además, se debe usar un argumento adicional que indique el nombre de los grupos, a saber, una lista con largo igual a la cantidad de grupos.

- **write_parcels:** Toma una lista de índices de triángulos (correspondientes a una parcela), y los guarda en un archivo binario con extensión .intersectiondata. 

Aunque no todas las funciones se encuentren documentadas, en general su uso es sencillo y sólo requiere un poco de ensayo y error.
