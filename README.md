Esto es un proyecto que tiene algunos scripts de python en los que se practica un poco con modelos de inteligencia artificial ejecutados con ficheros llamafile. 

El script más llamativo es market_test_pilot_product_speaker.py. 
En este script se presenta una situación imaginaria en la que una compañía ha sacado un producto piloto de un altavoz y quiere saber la opinión de los consumidores. 
Tenemos una base de datos local mysql con 10 reseñas sobre el altavoz. Tenemos cuatro topics que aparecen de forma salteada en las reseñas: design, shipping, price, maxVolume (una nueva feature).

El script coge cada reseña y se la pasa al modelo pidiéndole que genere una frase resumiendo la opinión de cada reseña en relación con cada uno de los 4 topics. Estos resultados se guardan en la misma base de datos en 4 columnas a continuación de la columna que contiene la review.

Una vez hecho este proceso, se le pasa al modelo todas las respuestas generadas en torno a cada topic para que nos genere una valoración global de cada topic, mencionando los puntos clave positivos y negativos. 

Esto puede ser muy útil como análisis de mercado para conocer la recepción de un producto piloto entre los consumidores. 

Es interesante ejecutarlo con distintos modelos para ver qué resultado nos da cada uno.