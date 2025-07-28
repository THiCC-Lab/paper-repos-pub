(clear-all)

(define-model test-add-values
(model-output "Testing Values-List Memory Add Function...")
(sgp :esc t :lf .05 :trace-detail medium)
(add-values-dm 
incident mix political  economic  social  environmental  cost implications potentially serious long-term effects 
 also  incidents multiagency and/or multijurisdictional 
 senior official  need aware ics interagency  regional  multiagency coordination systems work ensure cooperative response efforts 
document attempts acquaint senior officials national incident management system  nims   incident command system  ics   unified command  specific role within constructs 
end document  find ics readiness checklist  ics incident checklist  information after-action review well sample delegation authority letter 
frequently asked questions
 maintain control incident occurs 
senior official  establish overall policy  provide guidelines priorities  objectives  constraints qualified incident commander 
 many agencies  done matter policy written delegation authority 
  refer sample end document  
)
;; (chunk-type number value)
;; (chunk-type test1 slot1)
;; (chunk-type test2 slot1 (slot2 2))

;; (add-dm
;;     (isa number value 1)
;;     (two value 2)
;; )
;; (add-dm a b c)
;; ;; below should give warning, check what happens on HDM side
;; ;; shouldn't break anything, keep going
;; (add-dm
;;     (bad-chunk isa invalid-type)
;;     (bad-slot 10)
;; )
;; (add-dm (a isa test1) (b isa test2))
;; ;; (add-dm ("this is chunk e" isa test1 slot1 100))
;; (add-dm ())
)