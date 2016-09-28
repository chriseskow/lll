(load "_load-target.scm")

(print loaded-scalar) ; => foobar
(print (loaded-func 1 2)) ; => from function
