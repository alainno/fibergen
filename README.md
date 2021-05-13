# :microscope: Generador de micrografías artificiales de fibra de alpaca

El objetivo de este proyecto es generar imágenes artificiales o sintéticas para constituir un conjunto de datos que pueda ser utilizado para el entrenamiento de modelos de redes neuronales que identifiquen la calidad de la fibra de alpaca, a través de técnicas de visión artificial.

Las imágenes generadas son similares a la Figura 1, la cual muestra una micrografía real de fibra de alpaca obtenida con un equipo OFDA-2000 en el laboratorio de análisis de fibras del Proyecto Especial Camélidos Sudamericanos (PECSA) del Gobierno Regional de Puno.

![](img/sample-ofda.jpg)

*Figura 1: Micrografía real de fibra de alpaca.*

[comment]: <> (Ejemplo de fibra Medulómetro:)

[//]: (![](img/sample-medulometro.jpg))

La Figura 2 muestra un ejemplo de micrografía sintética, para esto se crea un algoritmo que dibuje líneas curvas en diferentes ubicaciones y de diferente grosor, todo de forma aleatoria.

![](img/sample-artificial.png)

*Figura 2: Ejemplo de micrografía sintética.*

### Etiquetas o ground truths

- Fibras delgadas y gruesas: [sample.py](sample.py)
- Mapas de distancia: [dm-gts.ipynb](dm-gts.ipynb)
- Skeletons: [skeletons-gts.ipynb](skeletons-gts.ipynb)
- Segmentación de instancias: [instances.ipynb](instances.ipynb)
- Segmentación semántica: [segmentation.ipynb](segmentation.ipynb)
 
### Scripts

- Clase para la abstraccion de muestras de fibra: [fiberrandom.py](fiberrandom.py)
- Funciones auxiliares: [functions.py](functions.py)