(load "./_helpers.scm")

(def (zero? n) (= n 0))
(def (decr n) (- n 1))
(def (fact n)
  (if (zero? n)
    1
    (* n (fact (decr n)))))

(assert 1 (fact 0))
(assert 1 (fact 1))
(assert 2 (fact 2))
(assert 6 (fact 3))
(assert 24 (fact 4))
(assert 120 (fact 5))
(assert 720 (fact 6))
