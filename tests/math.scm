(load "_helpers.scm")

; Addition
(assert 1 (+ 1))
(assert 1 (+ 0 1))
(assert 3.14159 (+ 3 0.14159))

; Subtraction
(assert 0 (- 0))
(assert 1 (- 1))
(assert 1 (- 2 1))
(assert 0 (- 3 2 1))
(assert -4 (- 1 5))
(assert-tolerance 0.14159 (- 3.14159 3) 0.000001)

; Multiplication
(assert 0 (* 0))
(assert 1 (* 1))
(assert 0 (* 0 1))
(assert 0 (* 0 1 2))
(assert 2 (* 1 2))
(assert 6 (* 1 2 3))
(assert -24 (* 1 2 3 -4))
(assert 12.0 (* 1 2 3 -4 -0.5))

; Combination
(assert -9 (+ 0 1 2 (* 3 4 (- 5 6))))
