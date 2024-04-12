Esto es un proyecto que tiene algunos scripts de python en los que se practica un poco con modelos de inteligencia artificial ejecutados con ficheros llamafile. 

Los scripts más llamativos son market_test_pilot_product_speaker.py y story_summary_reconstruction.

- market_test_pilot_product_speaker.py:

En este script se presenta una situación imaginaria en la que una compañía ha sacado un producto piloto de un altavoz y quiere saber la opinión de los consumidores. 
Tenemos una base de datos local mysql con 10 reseñas sobre el altavoz. Tenemos cuatro topics que aparecen de forma salteada en las reseñas: design, shipping, price, maxVolume (una nueva feature).

El script coge cada reseña y se la pasa al modelo pidiéndole que genere una frase resumiendo la opinión de cada reseña en relación con cada uno de los 4 topics. Estos resultados se guardan en la misma base de datos en 4 columnas a continuación de la columna que contiene la review.

Una vez hecho este proceso, se le pasa al modelo todas las respuestas generadas en torno a cada topic para que nos genere una valoración global de cada topic, mencionando los puntos clave positivos y negativos. 

Esto puede ser muy útil como análisis de mercado para conocer la recepción de un producto piloto entre los consumidores. 

Es interesante ejecutarlo con distintos modelos para ver qué resultado nos da cada uno.

- story_summary_reconstruction:

Este script le pide al modelo que genere una historia de entre 100 y 120 palabras. Después le pide que la resuma a 50-70 palabras. Seguidamente le pide que reconstruya la historia original usando entre 150 y 180 palabras. A continuación vuelve a pedirle que la resuma, esta vez usando entre 20 y 40 palabras. Finalmente le pide una última reconstrucción de 200 a 220 palabras. 

Con este script he querido investigar hasta qué punto los modelos pueden comprimir y expandir el tamaño de un texto manteniendo su sentido y significado. Es muy interesante ver los resultados utilizando distintos modelos y distintas temperaturas. Este script sirve para testar diferentes modelos y ver su capacidad de síntesis y análisis de un texto.