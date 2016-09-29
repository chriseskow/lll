(load "./_helpers.scm")

(def fib (lambda (n)
  (if (< n 2)
    n
    (+
      (fib (- n 1))
      (fib (- n 2))))))

(assert 0 (fib 0))
(assert 1 (fib 1))
(assert 1 (fib 2))
(assert 2 (fib 3))
(assert 3 (fib 4))
(assert 5 (fib 5))
(assert 8 (fib 6))
(assert 13 (fib 7))
(assert 21 (fib 8))
