(load "_helpers.scm")

; Equality
(assert 1 (= "" ""))
(assert 1 (= "foo" "foo"))
(assert 0 (= "foo" "bar"))
(assert 0 (= "123" 123))

; To-string
(assert "123" (to-string "123"))
(assert "123" (to-string 123))
(assert "123.45" (to-string 123.45))
(assert "<operator>" (to-string def))
(assert "<builtin>" (to-string to-string))
(assert "<lambda>" (to-string (lambda () 1)))
