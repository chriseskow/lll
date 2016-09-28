(load "_helpers.scm")

; Scalar value
(def PI 3.14159)
(assert 4.14159 (+ 2 2 (- PI 3)))

; Calculated value
(def ANSWER (+ 40 2))
(assert 42 ANSWER)

; Lexical scoping and rebinding
(def n 1)
(def f (lambda ()
  (assert 1 n)
  (def n 2)
  (assert 2 n)))
(f)
