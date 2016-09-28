(def debug-mode 0)

(def <= (lambda (x y)
  (if (< x y)
    1
    (if (= x y)
      1
      0))))

(def abs (lambda (x)
  (if (< x 0)
    (- 0 x)
    x)))

(def almost-equal? (lambda (x y tolerance)
  (<= (abs (- x y)) tolerance)))

(def assert-helper (lambda (comparator expected actual)
  (if (comparator)
    (if debug-mode
      (print "OK (" actual ")")
      1)
    (print "FAIL (expected: " expected ", actual: "  actual ")"))))

(def assert (lambda (expected actual)
  (assert-helper
    (lambda () (= expected actual))
    expected
    actual)))

(def assert-tolerance (lambda (expected actual tolerance)
  (assert-helper
    (lambda () (almost-equal? expected actual tolerance))
    expected
    actual)))
