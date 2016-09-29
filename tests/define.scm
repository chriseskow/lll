(load "./_helpers.scm")

; Scalar value
(define PI 3.14159)
(assert 4.14159 (+ 2 2 (- PI 3)))

; Calculated value
(define ANSWER (+ 40 2))
(assert 42 ANSWER)

; Function binding
(define n 1)
(define f (lambda ()
  (assert 1 n)
  (define n 2)
  (assert 2 n)))
(f)

; Function defineinition syntax
(define (g) 3)
(define (h x) (* x (g)))
(define (i x y)
  (* x y) ; Useless, but tests multiple-expression body
  (- x (h y)))
(assert 3 (g))
(assert 18 (h 6))
(assert -1 (i 20 7))
