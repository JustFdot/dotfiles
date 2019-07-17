;;; ~/.doom.d/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here


(map!
      :n "RET"       #'+evil/insert-newline-below
      :n [C-return]  #'+evil/insert-newline-above
      :n [S-return]  #'+evil/insert-newline-above

      (:map override
        "C-/"          #'swiper
        :m "gs"        #'avy-goto-char-timer)

      (:when (featurep! :completion company)
        :i "S-SPC"     #'+company/complete
        (:after company
          (:map company-active-map
            "C-j"      #'company-select-next-or-abort
            "C-k"      #'company-select-previous-or-abort)))

      (:when (featurep! :email mu4e)
        (:map mu4e-headers-mode-map
          "RET"        #'mu4e-headers-view-message))

      (:when (featurep! :editor fold)
        :nv "zr"       #'+fold/open-all)

      (:when (featurep! :emacs dired +ranger)
        :leader
          :desc "Open deer with file in buffer" "d" #'deer)
  )
