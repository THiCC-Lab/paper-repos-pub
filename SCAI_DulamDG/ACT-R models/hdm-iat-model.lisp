(clear-all)

(define-model iatmodel
    
; (sgp :seed (200 4))
; default (sgp :v t :esc t :act t) 
; param setting 1 (sgp :v t :esc t :rt -2 :lf 0.4 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 2(sgp :v t :esc t :rt -2 :lf 0.5 :bll 0.5 :act t :ncnar nil) 
; param setting 3 (sgp :v t :esc t :rt -2 :lf 0.5 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 4 (sgp :v t :esc t :rt -2 :lf 0.6 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 5 (sgp :v t :esc t :rt -2 :lf 0.3 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 6  (sgp :v t :esc t :rt -2 :lf 0.25 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 7  (sgp :v t :esc t :rt -2 :lf 0.15 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 8   (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.5 :bll 0.5 :act t :ncnar nil)
; param setting 9   (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.6 :bll 0.5 :act t :ncnar nil)
; param setting 10   (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.55 :bll 0.5 :act t :ncnar nil)
; param setting 11    (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.7 :bll 0.5 :act t :ncnar nil)
; param setting 12  (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.65 :bll 0.5 :act t :ncnar nil)
; param setting 13  (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.65 :bll 0.4 :act t :ncnar nil)
; param setting 14  (sgp :v t :esc t :rt -2 :lf 0.2 :ans 0.65 :bll 0.4 :act t )
; param setting 15   (sgp :v t :esc t :rt -1.8 :lf 0.2 :ans 0.65 :bll 0.4 :act t )
; param setting 16  14+ added base level activation for B chunks and set all to -0.15
; param setting 17  14+ added base level activation for B chunks and set all to -0.5
; param setting 18  14+ added base level activation for B chunks and set all to -1
; param setting 19  14+ added base level activation for B chunks and set all to -1, added W set to 1
; param setting 20  14+ added base level activation for B chunks and set all to -2, added W set to 1
; param setting 21  14+ added base level activation for B chunks and set all to -1, added W set to 1, added P set to 1, added N set to -1
; param setting 22  14+ added base level activation for B chunks and set all to -5, added W set to 1, added P set to 1, added N set to -1
; param setting 23  14+ added base level activation for B chunks and set all to -3, added W set to 2, added P set to 3, added N set to 3
; param setting 24  (sgp :v t :esc t :rt -2 :lf 0.21 :ans 0.65 :act t :bll 0.5)
; param setting 25 (sgp :v t :esc t :rt -2 :lf 0.19 :ans 0.5 :act t  :bll 0.5)
; param setting 26  (sgp :v t :esc t :rt -2 :lf 0.25 :ans 0.5 :bll 0.5 :act t )
; param setting 27 (sgp :v t :esc t :rt -2 :lf 0.25 :ans 0.5 :bll 0.55 :act t :ncnar nil)
; param 28 = 6 (best so far) added base level activation for B chunks and set all to -0.5, added W set to 0.5, added P set to 1, added N set to 1 -> individual chunks not working out, will check rt for correct and wrong, penalize wrong but not remove it
;  (sgp :v t :esc t :rt -2 :lf 0.25 :ans 0.5 :act t :ncnar nil)
; param setting 29 (sgp :v t :esc t :rt -2 :lf 0.22 :bll 0.5 :ans 0.5 :act t :ncnar nil)
; param setting 30 (sgp :v t :esc t :rt -2 :lf 0.22 :bll 0.5 :ans 0.6 :act t :ncnar nil)

; runn 2p6 : (sgp :v t :esc t :rt -2 :lf 0.22 :bll 0.5 :ol t :ans 0.6 :act t :ncnar nil)
; runn 2p6m1 ol 1 : 
; runn 2p6m2 ol 2 : 
; runn 2p6m3 ol t mas 2: 
; runn 2p6m4 ol t mas 1: 
; runn 2p6m4 ol t mas 1.5: 
; hdm direct setting (sgp :v t :esc t :rt -2 :lf 0.22 :bll 0.5 :ol t :mas 1.5 :ans 0.6 :act t :ncnar nil)
(sgp :v t :esc t :lf 0.2 :ncnar nil)
(chunk-type goal state block probe)
(chunk-type pair probe answer)
(chunk-type image probe race)
(chunk-type word probe valence)

(define-chunks zero positive negative block4 next start attending-target attending-probe testing)

(add-goal-dm  (goalm isa goal state zero))

(add-dm
; (goalm isa goal state zero)
 (black1 isa image probe "black1" race black) (black2 isa image probe "black2" race black) 
 (black3 isa image probe "black3" race black) (black4 isa image probe "black4" race black) 
 (black5 isa image probe "black5" race black) (white1 isa image probe "white1" race white) 
 (white2 isa image probe "white2" race white) (white3 isa image probe "white3" race white) 
 (white4 isa image probe "white4" race white) (white5 isa image probe "white5" race white)
 (good isa word probe "good" valence positive) (happy isa word probe "happy" valence positive) 
 (pleasure isa word probe "pleasure" valence positive)
 (love isa word probe "love" valence positive) (joy isa word probe "joy" valence positive)
 (bad isa word probe "bad" valence negative) (hurt isa word probe "hurt" valence negative) 
 (agony isa word probe "agony" valence negative) (evil isa word probe "evil" valence negative) 
 (nasty isa word probe "nasty" valence negative)
)

(install-device '("motor" "keyboard"))
(start-hand-at-keypad)
; (declare-buffer-usage imaginal imbuffer :all)
(p start-state "start state for every new model run"
    =goal>
      isa      goal
      state    zero
     ==>
    =goal>
      state    start 
      block 1 
   +visual>
      cmd      clear
)
(p attend-probe "start state for every stimulus"
    =goal>
      isa      goal
      state    start
    =visual-location>
    ?visual>
     state     free

   ==>
    +visual>               
      cmd      move-attention
      screen-pos =visual-location
    =goal>
      state    attending-probe
)

(p read-probe-block4 "switching from vcongruent to incongruent"
    =goal>
      isa      goal
      state    attending-probe
    =visual>
      isa      visual-object
      value    "block4"
     ?manual>   
      state    free
   ==>

    =goal>
      state    next
      block 4
    +visual>
      cmd      clear
      +manual>              
      cmd      press-key     
      key      "w"     
)


(p read-probe "attend probe for congruent"
    =goal>
      isa      goal
      state    attending-probe
    =visual>
      isa      visual-object
      value    =val
      - value    "block4"

   ==>
    =goal>
      state    testing
      probe    =val
    +retrieval>
       probe    =val
 
)

(p recall-image-black-2-3 "black image for congruent"
    =goal>
      isa      goal 
      state    testing
      probe    =val
      block    1 
    =retrieval>
      isa      image
      probe     =val
      race   black
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "d"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recall-image-black-4-5 "black image for incongruent"
    =goal>
      isa      goal 
      state    testing
      probe    =val
      block   4
    =retrieval>
      isa      image
      probe     =val
      race   black
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "a"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recall-image-white-2-3 "white image for congruent"
    =goal>
      isa      goal 
      state    testing
      probe    =val
      block   1 
    =retrieval>
      isa      image
      probe     =val
      race   white
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "a"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recall-image-white-4-5 "white image for incongruent"
    =goal>
      isa      goal 
      state    testing
      probe    =val
      block   4 
    =retrieval>
      isa      image
      probe     =val
      race   white
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "d"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recall-positive "positive valence word"
    =goal>
      isa      goal 
      state    testing
      probe    =val

    =retrieval>
      isa      word
      probe     =val
      valence   positive
    
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "a"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recall-negative "negative valence word"
    =goal>
      isa      goal 
      state    testing
      probe    =val
    =retrieval>
      isa      word
      probe     =val
      valence   negative
    ?manual>   
      state    free
    ?visual>
      state    free
   ==>
    +manual>              
      cmd      press-key     
      key      "d"
    =goal>
      state    next
    +visual>
      cmd      clear
)

(p recalled-wrong "only hdm cases"
    =goal>
      isa      goal 
      state    testing
     =retrieval>
      probe     =val
      - valence   negative
      - valence   positive
      - race black
      - race white
    ?visual>
      state    free
 ?manual>   
      state    free
   ==>
    =goal>
     state    next
    +visual>
     cmd      clear
     +manual>              
      cmd      press-key     
      key      "s"
)


(p cannot-recall "recall failure"
    =goal>
      isa      goal 
      state    testing
    ?retrieval>
      buffer   failure
    ?visual>
      state    free
 ?manual>   
      state    free
   ==>
    =goal>
     state    next
    +visual>
     cmd      clear
     +manual>              
      cmd      press-key     
      key      "w"
)


(p detect-end "after key pressed, reset to start state"
    =goal>
      isa      goal
      state    next


    ?visual>
      state    free
  ==>
   

   =goal>
      state    start  
   +visual>
      cmd      clear
)


(goal-focus goalm)
; (Set-similarities
;   (black1 black2 0.1) (black1 black3 0.1) (black1 black4 0.1) (black1 black5 0.1) 
;   (black2 black3 0.1)  (black2 black4 0.1)  (black2 black5 0.1)  (black3 black4 0.1)  (black3 black5 0.1) (black4 black5 0.1)
;   (white1 white2 0.1) (white1 white3 0.1) (white1 white4 0.1) (white1 white5 0.1) 
;   (white2 white3 0.1)  (white2 white4 0.1)  (white2 white5 0.1)  (white3 white4 0.1)  (white3 white5 0.1) (white4 white5 0.1)
;   (agony bad 0.1) (agony evil 0.1) (agony hurt 0.1) (agony nasty 0.1) 
;   (bad evil 0.1)  (bad hurt 0.1)  (bad nasty 0.1)  (evil hurt 0.1) (evil nasty 0.1) (hurt nasty 0.1)
;   (good happy 0.1) (good joy 0.1) (good love 0.1) (good pleasure 0.1) 
;   (happy joy 0.1)  (happy love 0.1)  (happy pleasure 0.1)  (joy love 0.1) (joy pleasure 0.1) (love pleasure 0.1))



; (sdp black1 :base-level -0.5)
; (sdp black2 :base-level -0.5)
; (sdp black3 :base-level -0.5)
; (sdp black4 :base-level -0.5)
; (sdp black5 :base-level -0.5)
; (sdp bad :base-level 1)
; (sdp hurt :base-level 1)
; (sdp agony :base-level 1)
; (sdp evil :base-level 1)
; (sdp nasty :base-level 1)
; (sdp white1 :base-level 0.5)
; (sdp white2 :base-level 0.5)
; (sdp white3 :base-level 0.5)
; (sdp white4 :base-level 0.5)
; (sdp white5 :base-level 0.5)
; (sdp joy  :base-level 1)
; (sdp love  :base-level 1)
; (sdp pleasure  :base-level 1)
; (sdp happy  :base-level 1)
; (sdp good  :base-level 1)
)