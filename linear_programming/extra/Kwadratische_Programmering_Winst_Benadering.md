
# Kwadratische Programmering voor het Benaderen van een Specifieke Winst

## Probleemstelling

Het doel is om de productiehoeveelheden van AquaSparkle (A) en BioBurst (B) zo aan te passen dat de totale winst zo dicht mogelijk bij 150 euro ligt, met behoud van de grondstoffenbeperkingen.

## Doelfunctie

De doelfunctie is $ (150 - (5A + 8B))^2 $, wat kan worden uitgeschreven als:
$$  22500 - 1500A - 2400B + 25A^2 + 40AB + 64B^2 $$

Omgezet naar matrixvorm voor kwadratische programmering:
- $ x = [A, B] $
- $ P = \begin{bmatrix} 25 & 20 \ 20 & 64 \end{bmatrix} $
- $ q = \begin{bmatrix} -1500 \ -2400 \end{bmatrix} $

De constante term (22500) is irrelevant voor de optimalisatie en wordt daarom weggelaten.

## Beperkingen

De productiebeperkingen zijn:
- $ 2A + B \leq 100 $ (Grondstof X)
- $ A + 3B \leq 90 $ (Grondstof Y)
- $ A \geq 0, B \geq 0 $ (Niet-negativiteit)

In matrixvorm voor kwadratische programmering:
- $ A_{constraint} = \begin{bmatrix} 2 & 1 \ 1 & 3 \ -1 & 0 \ 0 & -1 \end{bmatrix} $
- $ b_{constraint} = \begin{bmatrix} 100 \ 90 \ 0 \ 0 \end{bmatrix} $

## Implementatie in OSQP

Deze waarden kunnen direct worden gebruikt in de OSQP solver om de optimale productiehoeveelheden te vinden die het dichtst bij een winst van 150 euro liggen, met inachtneming van de gegeven beperkingen.
