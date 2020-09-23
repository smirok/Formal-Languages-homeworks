module mortal.

. . . 
isMan "Socrates". 
isMan "Katya".

isMortal X :- isMan X.
parent "Anya" "Nina".
parent "Ivan" "Nina". 
parent "Ivan" "Sveta". 
parent "Nina" "Masha".
parent "Nina" "Ilya".
parent "Sveta" "Petya".  

male "Ilya".
male "Ivan".
male "Petya".

grandparent X Y :- parent X Z, parent Z Y. 

grandson X Y :- grandparent X Y, male Y.

kakich A 0 A :- male 2 3.
