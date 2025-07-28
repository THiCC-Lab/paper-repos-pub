(clear-all)

(define-model add-tests
(model-output "Testing Memory Add Function...")
(sgp :esc t :lf .05 :trace-detail medium)
(chunk-type number value)
(chunk-type test1 slot1)
(chunk-type test2 slot1 (slot2 2))

(add-dm
    (isa number value 1)
    (two value 2)
)
(add-dm a b c)
;; below should give warning, check what happens on HDM side
;; shouldn't break anything, keep going
(add-dm
    (bad-chunk isa invalid-type)
    (bad-slot 10)
)
(add-dm (a isa test1) (b isa test2))
;; (add-dm ("this is chunk e" isa test1 slot1 100))
(add-dm ())
)