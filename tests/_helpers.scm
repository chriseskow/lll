(define (assert-helper comparator expected actual)
  (if (comparator)
    (print "OK (" actual ")")
    (print "FAIL (expected: " expected ", actual: "  actual ")")))

(define (assert expected actual)
  (assert-helper
    (lambda () (= expected actual))
    expected
    actual))

(define (assert-tolerance expected actual tolerance)
  (define (<= x y)
    (if (< x y)
      1
      (if (= x y)
        1
        0)))
  (define (abs x)
    (if (< x 0)
      (- 0 x)
      x))
  (define (almost-equal? x y tolerance)
    (<= (abs (- x y)) tolerance))
  (assert-helper
    (lambda () (almost-equal? expected actual tolerance))
    expected
    actual))
