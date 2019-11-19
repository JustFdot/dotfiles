;;; ~/.doom.d/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here


(map!
      :n "RET"       #'+evil/insert-newline-below
      :n [C-return]  #'+evil/insert-newline-above
      :n [S-return]  #'+evil/insert-newline-above
      :v "v"         #'er/expand-region

      (:map override
        "C-/"        #'swiper
        :m "gs"      #'avy-goto-char-timer)

      ;; (:when (featurep! er/expand-region)
      ;;   :leader
      ;;   :desc "Expand region at point" "e"
      ;;     "C-="  #'er/expand-region
      ;;     "C--"  #'er/contract-region
      ;;   )

      (:when (featurep! :completion company)
        :i "S-SPC"   #'+company/complete)

      (:when (featurep! :email mu4e)
        (:map mu4e-headers-mode-map
          "RET"      #'mu4e-headers-view-message))

      (:when (featurep! :emacs dired +ranger)
        :leader
          :desc "Open deer with file in buffer" "d" #'deer)
  )
