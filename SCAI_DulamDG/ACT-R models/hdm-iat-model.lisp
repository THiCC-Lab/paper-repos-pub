(clear-all)

(define-model iatmodel
    
(sgp :seed (200 4))
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

(p read-probe-block4 "switching from congruent to incongruent"
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

)