; No arguments
(def one (lambda () 1))
(print one) ; => <lambda>
(print (one)) ; => 1

; Single argument
(def identity (lambda (x) x))
(print (identity 333)) ; => 333

; Multiple arguments
(def first (lambda (x y) x))
(print (first 11 22)) ; => 11

; Combination
(def incr (lambda (n) (+ n 1)))
(print (incr (one))) ; => 2

; Anonymous invocation
(print ((lambda (x y) (* x y)) 5 6)) ; => 30

; Closure
(def make-multiplier (lambda (x)
  (lambda (y) (* x y))))
(def doubler (make-multiplier 2))
(def tripler (make-multiplier 3))
(print (doubler 1)) ; => 2
(print (doubler 2)) ; => 4
(print (doubler 3)) ; => 6
(print (tripler 1)) ; => 3
(print (tripler 2)) ; => 6
(print (tripler 3)) ; => 9
