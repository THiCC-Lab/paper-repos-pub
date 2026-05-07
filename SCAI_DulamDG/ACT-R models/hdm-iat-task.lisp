
(load-act-r-model "hdm-iat-model.lisp")


; Global variables to hold the participant's response, the time of
; that response, the possible stimuli, and the data from the 
; original experiment.
(defvar *response* nil)
(defvar *response-time* nil)
; (defvar *results* nil)
(defstruct trial stimulus response score rt)


(defvar *race* '("black1" "black2" "black3" "black4" "black5" "white1" "white2" "white3" "white4" "white5"))
(defvar *words* '("good" "happy" "pleasure" "love" "joy" "bad" "hurt" "agony" "evil" "nasty"))
(defvar *block1* '(("good" "a") ("happy" "a") ("pleasure" "a") ("love" "a") ("joy" "a")
                  ("bad" "d") ("hurt" "d") ("agony" "d") ("evil" "d") ("nasty" "d")))
(defvar *block2* '(("black1" "d") ("black2" "d") ("black3" "d") ("black4" "d") ("black5" "d")
                  ("white1" "a") ("white2" "a") ("white3" "a") ("white4" "a") ("white5" "a")))
(defvar *block4* '(("black1" "a") ("black2" "a") ("black3" "a") ("black4" "a") ("black5" "a")
                  ("white1" "d") ("white2" "d") ("white3" "d") ("white4" "d") ("white5" "d")))

(defvar *block3* (append *block1* *block2*))
(defvar *block5* (append *block1* *block4*))
(defvar *b4label* '(("block4" "d")))
(defvar *blocks* (list *block1* *block2* *block3* *b4label* *block4* *block5*))
(defvar *left-key*  "a")
(defvar *right-key* "d")
(defvar *error* "w")


(defun csv-field (x)
  (let ((s (princ-to-string (or x ""))))
    (if (or (find #\, s) (find #\" s) (find #\Newline s) (find #\Return s))
        (with-output-to-string (out)
          (write-char #\" out)
          (loop for ch across s do
                (when (char= ch #\") (write-char #\" out)) ; escape quotes
                (write-char ch out))
          (write-char #\" out))
        s)))

(defun save-result-to-csv (result filename run-id &optional (append-mode nil))
  (with-open-file (s filename
                     :direction :output
                     :if-exists (if append-mode :append :supersede)
                     :if-does-not-exist :create
                     :external-format :utf-8)
    (unless append-mode
      (format s "block,stimulus,response,score,rt,filename~%"))

    (loop for block in result
          for block-idx from 1 do
            (loop for tr across block do
              (format s  "~d,~a,~a,~d,~d,~d~%"
                      block-idx
                      (csv-field (trial-stimulus tr))
                      (csv-field (trial-response tr)) 
                      (trial-score tr)
                      (trial-rt tr)
                      (csv-field run-id)))))
  filename)

; do-experiment takes human true model false. It runs 5 blocks
; collecting the correctness and timing data per block, and then returns a list with lists where each sublist
; represents a block with the first item being % correct and the second mean response time.
(defun do-experiment (human)

  (if (and human (not (visible-virtuals-available?)))
      (print-warning "Cannot run the task as a person without a visible window available.")
    
    (progn

      ; create a varaible to hold the data, an indication of whether the
      ; model is performing the task, and an opened experiment window that
      ; is visible if a human is performing the task or virtual if it is
      ; a model.
      
      (let* ((result nil)
             (model (not human))
             (window (open-exp-window "IAT-Window" :visible human)))
        
        (when model
          (install-device window))
        

        (dotimes (i 6) 

          (let ((trials
             (make-array 0 :adjustable t :fill-pointer 0)))
           
            
            ; randomize the list of items to present which are taken from the possible pairs
            (dolist (x (permute-list (nth i *blocks*))) 
         
              ; clear the window and display the prompt
              (clear-exp-window window)
              (add-text-to-exp-window window (first x) :x 150 :y 150)
           
              ; clear the response and record the time when the trial is started
              (setf *response* nil)      
                         
              (let ((start (get-time model)))
    
                
                ; If it's the model run it for exactly 5 seconds or if it's a person wait for 5 seconds to finish
                (if model
                  (run-until-action "output-key")
                  (while (< (- (get-time nil) start) 3000)
                         (process-events)))
                
            
            (let* ((rt (- *response-time* start))
                   (correct (equal *response* (second x)))
                   (score (if correct 1 0)))
              (format t "Displayed: ~A |answer: ~A | Key: ~A | Score: ~A | RT: ~A~%" (first x) (second x) *response* score rt)
              (vector-push-extend
               (make-trial
                :stimulus (first x)
                :response *response*
                :score score
                :rt rt)
               trials))))

         
        (push trials result)))
            
        
        ; return the reversed result list so that it's in presentation order
        ; (since they were pushed onto the list).
    
         (reverse result)))))
 
; paired-task takes two required parameters: the number of stimuli to
; present in a block and the number of blocks to run.  The optional 
; parameter if specified as true will run a person instead of the model.

(defun paired-task (&optional human)

  ; Create a command for the respond-to-key-press function so that
  ; it can be used to monitor "output-key".
  
  (add-act-r-command "paired-response" 'respond-to-key-press 
                     "Paired associate task key press response monitor")
  (monitor-act-r-command "output-key" "paired-response")
  
  ; Run the function that does the actual experiment, return the result
  ; of that, and remove the monitor and command that were added.
  
  (prog1 

    (setf *results* (do-experiment human))

    (remove-act-r-command-monitor "output-key" "paired-response")
    (remove-act-r-command "paired-response")))


; respond-to-key-press will record the time of a key press
; using get-time (which reports model time if passed a true
; value or real time if passed nil, and model will be nil
; if it is a person performing the task) and the key that 
; was pressed.

(defun respond-to-key-press (model key)
 
  (setf *response-time* (get-time model))
  (setf *response* key))


    (format t "Saved: ~a~%" outfile)))
(defun make-timestamped-filename (base-name &optional (extension "csv")) 
  (multiple-value-bind (second minute hour day month year) 
    (decode-universal-time (get-universal-time)) 
    (format nil "~a_~4,'0d~2,'0d~2,'0d_~2,'0d~2,'0d~2,'0d.~a" 
        base-name year month day hour minute second extension) )) 

(defun run-once ()
(format t "inside run once 1")
(let ((outfile (make-timestamped-filename "hdm-iat.csv"))) 
  (format t "inside run once 2")
      (let ((results (paired-task)))
            (format t "inside run once n")

        (save-result-to-csv
         results
         outfile
         "run1")  

        (format t "Finished run1"))

    (format t "Saved: ~a~%" outfile)))

(add-act-r-command "run-once" 'run-once "Run once and save data in excel")

; (run-once)




