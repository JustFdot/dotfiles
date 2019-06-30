;;; ~/.doom.d/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here


(map! (:map override
        "C-/"         #'swiper
        :m "gs"       #'avy-goto-char-timer
        :n "RET"      #'+evil/insert-newline-below
        :n [C-return] #'+evil/insert-newline-above
        :n [S-return] #'+evil/insert-newline-above)
      (:when (featurep! :completion company)
        :i "S-SPC"    #'+company/complete)
      (:when (featurep! :editor fold)
        :nv "zr"      #'+fold/open-all)
      (:when (featurep! :emacs dired +ranger)
        :leader
          :desc "Open deer with file in buffer" "d" #'deer)
  )
