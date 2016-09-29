(load "./_helpers.scm")

(define n 3)
(assert (quote ()) (list))
(assert (quote (1)) (list 1))
(assert (quote (1 2)) (list 1 2))
(assert (quote (1 2 3)) (list 1 2 n))
(assert (quote (1 2 3 4)) (list 1 2 n (+ 1 n)))
