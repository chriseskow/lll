; Addition
(print (+ 1)) ; => 1
(print (+ 0 1)) ; => 1
(print (+ 3 0.14159)) ; => 3.14159

; Subtraction
(print (- 0)) ; => 0
(print (- 1)) ; => 1
(print (- 2 1)) ; => 1
(print (- 3 2 1)) ; => 0
(print (- 1 5)) ; => -4
(print (- 3.14159 3)) ; => 0.14159

; Multiplication
(print (* 0)) ; => 0
(print (* 1)) ; => 1
(print (* 0 1)) ; => 0
(print (* 0 1 2)) ; => 0
(print (* 1 2)) ; => 2
(print (* 1 2 3)) ; => 6
(print (* 1 2 3 -4)) ; => -24
(print (* 1 2 3 -4 -0.5)) ; => 12.0

; Combination
(print (+ 0 1 2 (* 3 4 (- 5 6)))) ; => -9
