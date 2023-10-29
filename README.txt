Para poder ejecutar los experimentos correctamente debemos abrir al archivo 'main.py'. Es muy importante que se ejecute con el archivo
'abia_bicing.py' (que no se incluye en la entrega porqué forma parte del enunciado) en la misma carpeta, para que se pueda tenera acceso a las clases 'Estacion' y 'Estaciones'.

A partir de la linea 70 se encuentran las llamadas a las funciones que ejecutan los experimentos. Todas las llamadas tienen el siguiente formato: experimentoX(), donde X es el número del experimento.

Todas las llamadas a las funciones de los experimentos se encuentran comentadas, para poder ejecutarlas se debe descomentar la llamada a la función que se desea ejecutar.

El resto de líneas (con declaraciones de variables, etc) no se deben comentar, ya que son los valores obtenidos como resultado en los experimentos y que se utilizan para los otros experimentos.

Las variables declaradas en el archivo son para realizar las ejecuciones de los experimentos con los valores mostrados en el informe.
En algunos experimentos hay múltiples valores mostrados en el informe, pero aqui solo se ejecutan con uno de ellos.

El experimento 5 es el único que se tiene que ejecutar 2 veces, una para cada heurístico. Para cambiar el heurístico se debe abrir el
archivo 'parameters_bicing.py' y en la declaración del objeto 'params' se debe cambiar el valor del parametro 'coste_transporte' a False (heurístico 1) o True (heurístico 2).

Una vez realizadas las ejecuciones de los experimentos, se pueden realizar ejecuciones individuales del algoritmo Hill Climbing con una sola réplica
para ver el visualizador de rutas implementado en Pygame y los __repr__()/__str__() del estado inicial y el estado final solucionado.
Para cambiar el heurístico de cualquier ejecución se debe hacer en 'parameters_bicing.py' como se ha explicado anteriormente.