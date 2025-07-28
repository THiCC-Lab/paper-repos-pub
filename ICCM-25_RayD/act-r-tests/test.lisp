;; basic code to test flow of simple_declarative.py
(clear-all)
(define-model test
(sgp :esc t :lf 0.2 :hdm-v nil :trace-detail medium :time-scale 10e-8)
;; :pull-slots t :slot-pulling-approach top-n-with-threshold :slot-pulling-n 3
;; :slot-pulling-threshold 0.1)
(chunk-type message text)
(chunk-type song-lyrics lyrics-song-name lyrics (writer anonymous) 
    (genre unspecified))
;; (chunk-type song-lyrics lyrics-song-name lyrics)
(chunk-type get-song mode song-name)
(chunk-type artist name age genre most-popular)
;; (add-goal-dm (get-hw-song ISA get-song mode loading song-name hello-world))
(define-chunks (get-hw-song ISA get-song mode loading song-name hello-world)) ;;hello-world))
(add-dm
    (test-hello-world ISA message text "hello world, programmed to work but not to feel!")
    (hw ISA song-lyrics 
        lyrics-song-name hello-world 
        lyrics "hello world, programmed to work but not to feel!"
        writer "Louie Zhong"
        genre lyrical
    )
    (gf ISA song-lyrics
        lyrics-song-name girlfriend
        lyrics "You say, I want to be your girlfriend"
        writer "hemlocke springs"
        genre indie
    )
    (hw-song ISA song-lyrics
        lyrics-song-name hello-world-two
        lyrics "not even sure that this is real"
    )
    (artist1 ISA artist 
        name "hemlocke springs"
        age 23
        genre indie
        most-popular girlfriend
    )

    ;; (s1 ISA sing-song singing h)
    
)
;; (write-line "this thing on?")


;; (p print-text
;;     =goal>
;;         ISA  message
;;         text =message-text
;;     ==>
;;     -goal>
;;     !output! (=message-text) 
;; )
(p print-from-memory
    =goal>
        ISA  get-song
        mode printing
        song-name =song1
    =retrieval>
        ;; Note: change below depending on how slot pulling works
        ;; ISA song-lyrics
        ;; song-name =song1
        lyrics =song-lyrics
        ;; writer =song-writer
        ;; genre  =song-genre
    ==>
    -goal> 
    -retrieval>
    !output! (=song-lyrics)
)
(p load-song
    =goal>
        ISA       get-song
        song-name =song1
        mode      loading
    ?retrieval>
        buffer empty
==>
    =goal>
        ISA get-song
        song-name  =song1
        mode printing
    +retrieval>
        ;; ISA       song-lyrics
        ;; genre !indie
        lyrics-song-name =song1
        ;; lyrics unknown 
        ;; :slot-pull nil
        ;; these DM-type parameters modify what retrieval is doing - can I use
        ;; this for HDM?
        ;; :unknown full-song-lyrics
        ;; :CT 0
        ;; :recently-retrieved nil
        ;; :lf 1
)
;; (goal-focus hello-world)
(goal-focus get-hw-song)
)