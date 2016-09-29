(load "./_helpers.scm")

; Scalar value
(def PI 3.14159)
(assert 4.14159 (+ 2 2 (- PI 3)))

; Calculated value
(def ANSWER (+ 40 2))
(assert 42 ANSWER)

; Function binding
(def n 1)
(def f (lambda ()
  (assert 1 n)
  (def n 2)
  (assert 2 n)))
(f)

; Function definition syntax
(def (g) 3)
(def (h x) (* x (g)))
(def (i x y)
  (* x y) ; Useless, but tests multiple-expression body
  (- x (h y)))
(assert 3 (g))
(assert 18 (h 6))
(assert -1 (i 20 7))
