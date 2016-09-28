(load "_helpers.scm")

; No arguments
(def one (lambda () 1))
(assert 1 (one))

; Single argument
(def identity (lambda (x) x))
(assert 333 (identity 333))

; Multiple arguments
(def first (lambda (x y) x))
(assert 11 (first 11 22))

; Combination
(def incr (lambda (n) (+ n 1)))
(assert 2 (incr (one)))

; Anonymous invocation
(assert 30 ((lambda (x y) (* x y)) 5 6))

; Closure
(def make-multiplier (lambda (x)
  (lambda (y) (* x y))))
(def doubler (make-multiplier 2))
(def tripler (make-multiplier 3))
(assert 2 (doubler 1))
(assert 4 (doubler 2))
(assert 6 (doubler 3))
(assert 3 (tripler 1))
(assert 6 (tripler 2))
(assert 9 (tripler 3))
