(load "./_helpers.scm")

; Comparison
(assert -1 (<=> 1 2))
(assert 0 (<=> 1 1))
(assert 1 (<=> 2 1))

; Equality
(assert 0 (= 1 2))
(assert 0 (= 1 2 3))
(assert 1 (= 1 1))
(assert 1 (= 1 1 1))

; Less than
(assert 1 (< 1 2))
(assert 0 (< 2 1))
(assert 0 (< 1 1))
