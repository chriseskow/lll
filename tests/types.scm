(load "./_helpers.scm")

(assert "symbol" (type (quote x)))
(assert "int" (type 42))
(assert "float" (type 3.14159))
(assert "string" (type "foobar"))
(assert "list" (type (list 1 2)))
(assert "operator" (type define))
(assert "builtin" (type type))
(assert "lambda" (type (lambda (x) x)))
