(def zero? (lambda (n) (= n 0)))
(def decr (lambda (n) (- n 1)))
(def fact (lambda (n)
  (if (zero? n)
    1
    (* n (fact (decr n))))))

(print (fact 0)) ; => 1
(print (fact 1)) ; => 1
(print (fact 2)) ; => 2
(print (fact 3)) ; => 6
(print (fact 4)) ; => 24
(print (fact 5)) ; => 120
(print (fact 6)) ; => 720
