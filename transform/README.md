Affine Transform
======================
Este código aplica una matriz de transformación afín a curvas en <a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\mathbb{R}^3" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;\mathbb{R}^3" title="\large \mathbb{R}^3" /></a>. Su utilidad en este caso es mover fibras cerebrales de un espacio a otro (por ejemplo, de T2 a Talairach).

## Datos de ejemplo
En el siguiente enlace hay un sujeto de la base de datos ARCHI, con sus fibras remuestreadas a 21 puntos por fibra.
https://drive.google.com/drive/folders/1-qYE4iCXVQHoxkwSgcqW1V2ExnsSvk4D?usp=sharing

- fibras_input.bundles: Archivo tractografía de entrada, a la cual se le aplicará la matriz.
- fibras_output.bundles: Archivo en el cual se guardará la tractografía transformada.
- matriz_transformacion.trm: Archivo que contiene la matriz de transformación afín a aplicar a la tractografía.

## Ejemplo de uso

Compilar:
```
g++ -std=c++14 -O3 transform.cpp -o transform -fopenmp -ffast-math
```
Ejecutar:
```
./transform input_bundles_folder/ output_bundles_folder/ transformation_matrix.trm 
```

## Parámetros de entrada
- **input_bundles_folder**: Carpeta que contiene los archivos .bundles a transformar. Si la carpeta contiene más de un archivo, la transformación se aplica a todos.
- **output_bundles_folder**: Carpeta en la que se guardarán los archivos .bundles transformados.
- **transformation_matrix.trm**: Matriz afín de transformación a aplicar sobre las fibras, en formato .trm.

## Formato de datos de entrada/salida
### Matriz de transformación
Una matriz de transformación afín en coordenadas homogéneas se escribe como:

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;M=\begin{bmatrix}&space;a&space;&&space;b&space;&&space;c&space;&&space;x\\&space;d&space;&&space;e&space;&&space;f&space;&&space;y\\&space;g&space;&&space;h&space;&&space;i&space;&&space;z\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;M=\begin{bmatrix}&space;a&space;&&space;b&space;&&space;c&space;&&space;x\\&space;d&space;&&space;e&space;&&space;f&space;&&space;y\\&space;g&space;&&space;h&space;&&space;i&space;&&space;z\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" title="\large M=\begin{bmatrix} a & b & c & x\\ d & e & f & y\\ g & h & i & z\\ 0 & 0 & 0 & 1 \end{bmatrix}" /></a>

Donde <a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;a,b,c,d,e,f,g,h,i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;a,b,c,d,e,f,g,h,i" title="\large a,b,c,d,e,f,g,h,i" /></a> son componentes de rotación y escalado, y <a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;x,y,z" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;x,y,z" title="\large x,y,z" /></a> son componentes de traslación.

Sin embargo, la matriz en formato .trm está escrita de acuerdo a las convenciones de Anatomist, por lo que se escribe:

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;M_{trm}=\begin{bmatrix}&space;x&space;&&space;y&space;&&space;z\\&space;a&space;&&space;b&space;&&space;c\\&space;d&space;&&space;e&space;&&space;f\\&space;g&space;&&space;h&space;&&space;i&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;M_{trm}=\begin{bmatrix}&space;x&space;&&space;y&space;&&space;z\\&space;a&space;&&space;b&space;&&space;c\\&space;d&space;&&space;e&space;&&space;f\\&space;g&space;&&space;h&space;&&space;i&space;\end{bmatrix}" title="\large M_{trm}=\begin{bmatrix} x & y & z\\ a & b & c\\ d & e & f\\ g & h & i \end{bmatrix}" /></a>

Entonces, por ejemplo, para aplicar un escalado con un factor 2, y una traslación de (5,10,15), la matriz afín sería:

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;M_{trm}=\begin{bmatrix}&space;2&space;&&space;0&space;&&space;0&space;&&space;5\\&space;0&space;&&space;2&space;&&space;0&space;&&space;10\\&space;0&space;&&space;0&space;&&space;2&space;&&space;15\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;M_{trm}=\begin{bmatrix}&space;2&space;&&space;0&space;&&space;0&space;&&space;5\\&space;0&space;&&space;2&space;&&space;0&space;&&space;10\\&space;0&space;&&space;0&space;&&space;2&space;&&space;15\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" title="\large M_{trm}=\begin{bmatrix} 2 & 0 & 0 & 5\\ 0 & 2 & 0 & 10\\ 0 & 0 & 2 & 15\\ 0 & 0 & 0 & 1 \end{bmatrix}" /></a>

Pero la matriz en formato .trm a usar en el código sería:

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;M_{trm}=\begin{bmatrix}&space;5&space;&&space;10&space;&&space;15\\&space;2&space;&&space;0&space;&&space;0\\&space;0&space;&&space;2&space;&&space;0\\&space;0&space;&&space;0&space;&&space;2&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\large&space;M_{trm}=\begin{bmatrix}&space;5&space;&&space;10&space;&&space;15\\&space;2&space;&&space;0&space;&&space;0\\&space;0&space;&&space;2&space;&&space;0\\&space;0&space;&&space;0&space;&&space;2&space;\end{bmatrix}" title="\large M_{trm}=\begin{bmatrix} 5 & 10 & 15\\ 2 & 0 & 0\\ 0 & 2 & 0\\ 0 & 0 & 2 \end{bmatrix}" /></a>


