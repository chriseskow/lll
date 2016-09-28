(load "_helpers.scm")

(assert 20 (if 0 10 20))
(assert 20 (if 0.0 10 20))
(assert 10 (if 1 10 20))
(assert 10 (if 123 10 20))
(assert 10 (if 123.45 10 20))

(assert 10 (if (= 1 1) 10 20))
(assert 20 (if (= 1 2) 10 20))
