Para poder ejecutar los experimentos correctamente debemos abrir al archivo 'main.py'.

A partir de la linea 70 se encuentran las llamadas a las funciones que ejecutan los experimentos. Todas las llamadas tienen el siguiente formato: experimentoX(), donde X es el número del experimento.

Todas las llamadas a las funciones de los experimentos se encuentran comentadas, para poder ejecutarlas se debe descomentar la llamada a la función que se desea ejecutar.

El resto de líneas (con declaraciones de variables, etc) no se deben comentar, ya que son los valores obtenidos como resultado en los experimentos y que se utilizan para los otros experimentos.

Las variables declaradas en el archivo son para realizar las ejecuciones de los experimentos con los valores mostrados en el informe.
En algunos experimentos hay múltiples valores mostrados en el informe, pero aqui solo se ejecutan con uno de ellos.

El experimento 6 es el único que se tiene que ejecutar 2 veces, una para cada heurístico. Para cambiar el heurístico se debe abrir el
archivo 'parameters_bicing.py' y en la declaración del objeto 'params' se debe cambiar el valor del parametro 'coste_transporte' a False (heurístico 1) o True (heurístico 2).