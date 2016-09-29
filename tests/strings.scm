(load "./_helpers.scm")

; Equality
(assert 1 (= "" ""))
(assert 1 (= "foo" "foo"))
(assert 0 (= "foo" "bar"))
(assert 0 (= "12" 12))

; to-string
(assert "23" (to-string "23"))
(assert "34" (to-string 34))
(assert "4.5" (to-string 4.5))
(assert "<operator>" (to-string def))
(assert "<builtin>" (to-string to-string))
(assert "<lambda>" (to-string (lambda () 1)))

; repr
(assert "\"56\"" (repr "56"))
(assert "67" (repr 67))
(assert "7.8" (repr 7.8))
(assert "<operator>" (repr def))
(assert "<builtin>" (repr repr))
(assert "<lambda>" (repr (lambda () 1)))
