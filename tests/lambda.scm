(load "./_helpers.scm")

; No arguments
(define one (lambda () 1))
(assert 1 (one))

; Single argument
(define identity (lambda (x) x))
(assert 333 (identity 333))

; Multiple arguments
(define first (lambda (x y) x))
(assert 11 (first 11 22))

; Combination
(define incr (lambda (n) (+ n 1)))
(assert 2 (incr (one)))

; Anonymous invocation
(assert 30 ((lambda (x y) (* x y)) 5 6))

; Closure
(define make-multiplier (lambda (x)
  (lambda (y) (* x y))))
(define doubler (make-multiplier 2))
(define tripler (make-multiplier 3))
(assert 2 (doubler 1))
(assert 4 (doubler 2))
(assert 6 (doubler 3))
(assert 3 (tripler 1))
(assert 6 (tripler 2))
(assert 9 (tripler 3))
