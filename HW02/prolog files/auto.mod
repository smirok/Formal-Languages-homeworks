module auto.

state "a".
state "b".
state "c".

initial "a".

final "a".

makes0 0.
makes0 3.
makes0 6.
makes0 9.

makes1 1.
makes1 4.
makes1 7.

makes2 2.
makes2 5.
makes2 8.

next "a" "b".
next "b" "c". 
next "c" "a".

transition A X A :- state A, makes0 X.
transition A X B :- 
  state A, state B, makes1 X, next A B. 
transition B X A :- 
  state A, state B, makes2 X, next A B.

runAuto Word :- initial S, runAux Word S.

runAux nil S :- final S. 
runAux [H | T] S :- transition S H S1, runAux T S1. 

