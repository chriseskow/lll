(def (assert-helper comparator expected actual)
  (if (comparator)
    (print "OK (" actual ")")
    (print "FAIL (expected: " expected ", actual: "  actual ")")))

(def (assert expected actual)
  (assert-helper
    (lambda () (= expected actual))
    expected
    actual))

(def (assert-tolerance expected actual tolerance)
  (def (<= x y)
    (if (< x y)
      1
      (if (= x y)
        1
        0)))
  (def (abs x)
    (if (< x 0)
      (- 0 x)
      x))
  (def (almost-equal? x y tolerance)
    (<= (abs (- x y)) tolerance))
  (assert-helper
    (lambda () (almost-equal? expected actual tolerance))
    expected
    actual))
