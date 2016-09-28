(def fib (lambda (n)
  (if (< n 2)
    n
    (+
      (fib (- n 1))
      (fib (- n 2))))))

(print (fib 0)) ; => 0
(print (fib 1)) ; => 1
(print (fib 2)) ; => 1
(print (fib 3)) ; => 2
(print (fib 4)) ; => 3
(print (fib 5)) ; => 5
(print (fib 6)) ; => 8
(print (fib 7)) ; => 13
(print (fib 8)) ; => 21
