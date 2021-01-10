Parcellation + Evaluation
======================
En esta carpeta se encuentran todos los códigos referentes a la parcelación en sí, además de aquellos utilizados para la evaluación cuantitativa.

## Dependencias
- Numpy: https://numpy.org/
- Networkx: https://networkx.github.io/

El código a ejecutar corresponde a **parcellation.py**. A diferencia de otros códigos que se ejecutan desde la terminal con argumentos de entrada (FFClust, Segmentación, etc), este código está escrito para ejecutarse de manera más parecida a un Jupyter Notebook. Por esto, las rutas de clusters/mallado/etc deben editarse directamente del código, y luego ejecutarlo todo o por partes. El resto de los códigos que se encuentran en la carpeta se llaman/ejecutan desde el script principal según se va necesitando.

El código se encuentra comentado para explicar el rol y funcionalidad de cada sección. Sin embargo, en términos generales:

- De entrada se requieren las intersecciones obtenidas previamente (archivos .intersectiondata), el nombre de los clusters correspondientes, y los mallados corticales sobre los que se proyectarán los resultados. 

- De salida el código obtiene una parcelación de la corteza cerebral según la intersección de los distintos clusters obtenidos previamente. Esta información se guarda en archivos binarios de .intersectiondata, que corresponden cada uno a la lista de triángulos del mallado cortical que pertenecen a una parcela en particular.

No hay mucho más que comentar. La explicación "teórica" del procedimiento de la parcelación (cálculo de mapas de densidad, traslape entre parcelas, etc) se encuentra en mi MT (https://drive.google.com/file/d/1nqThr1pLAG3f_H_2OSqMHNh5OAFZwMrY/view?usp=sharing). 

En cuanto a la evaluación cuantitativa, lo realizado también se encuentra explicado en mi MT. Dentro de la carpeta _evaluation_ se encuentran tanto los 3 atlas utilizados (Brainnetome, Lefranc, López) como también dos scripts:

- **mni_labelling.py:** Realiza el preprocesamiento necesario para obtener las etiquetas de cada triángulo del mallado cortical. Esto es necesario ya que los 3 atlas guardan los resultados de sus parcelaciones de manera distinta; en particular, en el caso de Brainnetome es una imagen en espacio MNI donde cada vóxel posee una etiqueta según la parcela a la que corresponda, por lo que primero se debe proyectar esta imagen a un mallado poligonal. Los casos de Lefranc y López son más sencillos ya que corresponden a vértices etiquetados.

- **dice_comparison.py:** Ejecuta la comparación cuantitativa entre la parcelación propia y alguno de los atlas previamente definido. Para esto se utiliza el coeficiente de Dice (DSC) entre pares de parcelas, guardando aquellas que superen un cierto umbral de significancia. 

Estos códigos también debiesen ejecutarse desde un IDE (en vez de desde la terminal), por lo que las rutas correspondientes deben editarse directamente desde el script.

Full Disclosure
======================
Originalmente, en mi MT iba a utilizar un código de parcelación ya escrito, lo cuál no fue posible debido a la implementación limitada y restringida de dicho script (requería exclusivamente fascículos segmentados y no clusters, además de requerir un formato específico en el registro de intersecciones y regiones preliminares). Esto, sumado a que me encontraba bastante cerca de la fecha límite, resultaron en que esta implementación de la parcelación fue hecha en un lapso de tiempo muy corto. Por lo tanto, es una implementación bastante primitiva, es probable que sea propensa a varios errores, y no entregue los mejores resultados. Lo positivo es que es infinitamente mejorable y optimizable, por lo que espero que al menos sirva como base para una mejor implementación a futuro, esto es, no necesariamente el código en sí, si no que las ideas y "lógicas" utilizadas aquí. 

  Finalmente, mi recomendación al que pretenda intentar trabajar con parcelaciones: por favor escribe una implementación que utilice programación orientada a objetos. Al menos a mi me hubiese ahorrado muchos dolores de cabeza.
