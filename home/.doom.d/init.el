;;; init.el -*- lexical-binding: t; -*-

;; Copy this file to ~/.doom.d/init.el or ~/.config/doom/init.el ('doom
;; quickstart' will do this for you). The `doom!' block below controls what
;; modules are enabled and in what order they will be loaded. Remember to run
;; 'doom refresh' after modifying it.
;;
;; More information about these modules (and what flags they support) can be
;; found in modules/README.org.

(doom! :input
       ;;chinese
       ;;japanese

       :completion
       company          ; the ultimate code completion backend
       ;;helm            ; the *other* search engine for love and life
       ;;ido             ; the other *other* search engine...
       ivy               ; a search engine for love and life

       :ui
       ;;deft              ; notational velocity for Emacs
       doom              ; what makes DOOM look the way it does
       doom-dashboard    ; a nifty splash screen for Emacs
       doom-quit         ; DOOM quit-message prompts when you quit Emacs
       ;;fill-column       ; a `fill-column' indicator
       hl-todo           ; highlight TODO/FIXME/NOTE/DEPRECATED/HACK/REVIEW
       ;;hydra
       ;;indent-guides     ; highlighted indent columns
       modeline          ; snazzy, Atom-inspired modeline, plus API
       ;;nav-flash         ; blink cursor line after big motions
       neotree           ; a project drawer, like NERDTree for vim
       ophints           ; highlight the region an operation acts on
       (popup +defaults)   ; tame sudden yet inevitable temporary windows
       ;;pretty-code       ; ligatures or substitute text with pretty symbols
       ;;tabs              ; an tab bar for Emacs
       ;;treemacs          ; a project drawer, like neotree but cooler
       ;;unicode           ; extended unicode support for various languages
       vc-gutter         ; vcs diff in the fringe
       vi-tilde-fringe   ; fringe tildes to mark beyond EOB
       ;;window-select     ; visually switch windows
       workspaces        ; tab emulation, persistence & separate workspaces
       ;;zen               ; distraction-free coding or writing

       :editor
       (evil +everywhere); come to the dark side, we have cookies
       file-templates    ; auto-snippets for empty files
       fold              ; (nigh) universal code folding
       ;;(format +onsave)  ; automated prettiness
       ;;lispy             ; vim for lisp, for people who dont like vim
       multiple-cursors  ; editing in many places at once
       ;;objed             ; text object editing for the innocent
       ;;parinfer          ; turn lisp into python, sort of
       rotate-text       ; cycle region at point between text candidates
       snippets          ; my elves. type so I don't have to


       :emacs
       (dired            ; making dired pretty [functional]
        +ranger         ; bringing the goodness of ranger to dired
       ;;+icons          ; colorful icons for dired-mode
        )
       undo              ; persistent, smarter undo for your inevitable mistakes
       electric          ; smarter, keyword-based electric-indent
       vc                ; version-control and Emacs, sitting in a tree

       :term
       ;;eshell            ; a consistent, cross-platform shell (WIP)
       ;;term              ; terminals in Emacs
       ;;vterm             ; another terminals in Emacs

       :checkers
       syntax              ; tasing you for every semicolon you forget
       ;;spell             ; tasing you for misspelling mispelling
       ;;grammar           ; tasing grammar mistake every you make

       :tools
       ;;ansible
       ;;debugger          ; FIXME stepping through code, to help you add bugs
       ;;direnv
       ;;docker
       ;;editorconfig      ; let someone else argue about tabs vs spaces
       ;;ein               ; tame Jupyter notebooks with emacs
       (eval +overlay)     ; run code, run (also, repls)
       ; flycheck          ; tasing you for every semicolon you forget
       ;;flyspell          ; tasing you for misspelling mispelling
       ;;gist              ; interacting with github gists
       lookup           ; helps you navigate your code and documentation
       ;;lsp
       ;;macos             ; MacOS-specific commands
       magit             ; a git porcelain for Emacs
       ;;make              ; run make tasks from Emacs
       ;;pass              ; password manager for nerds
       ;;pdf               ; pdf enhancements
       ;;prodigy           ; FIXME managing external services & code builders
       ;;rgb               ; creating color strings
       ;;terraform         ; infrastructure as code
       ;;tmux              ; an API for interacting with tmux
       ;;upload            ; map local to remote projects via ssh/ftp
       ;;wakatime

       :lang
       ;;agda              ; types of types of types of types...
       ;;assembly          ; assembly for fun or debugging
       ;;cc                ; C/C++/Obj-C madness
       ;;clojure           ; java with a lisp
       ;;common-lisp       ; if you've seen one lisp, you've seen them all
       ;;coq               ; proofs-as-programs
       ;;crystal           ; ruby at the speed of c
       ;;csharp            ; unity, .NET, and mono shenanigans
       data              ; config/data formats
       ;;erlang            ; an elegant language for a more civilized age
       ;;elixir            ; erlang done right
       ;;elm               ; care for a cup of TEA?
       emacs-lisp        ; drown in parentheses
       ;;ess               ; emacs speaks statistics
       ;;fsharp           ; ML stands for Microsoft's Language
       ;;go                ; the hipster dialect
       ;;(haskell +intero) ; a language that's lazier than I am
       ;;hy                ; readability of scheme w/ speed of python
       ;;idris             ;
       ;;(java +meghanada) ; the poster child for carpal tunnel syndrome
       javascript        ; all(hope(abandon(ye(who(enter(here))))))
       ;;julia             ; a better, faster MATLAB
       ;;kotlin            ; a better, slicker Java(Script)
       ;;latex             ; writing papers in Emacs has never been so fun
       ;;ledger            ; an accounting system in Emacs
       ;;lua               ; one-based indices? one-based indices
       markdown          ; writing docs for people to ignore
       ;;nim               ; python + lisp at the speed of c
       ;;nix               ; I hereby declare "nix geht mehr!"
       ;;ocaml             ; an objective camel
       (org              ; organize your plain life in plain text
        +attach          ; custom attachment system
        +babel           ; running code in org
        +capture         ; org-capture in and outside of Emacs
        +export          ; Exporting org to whatever you want
        +habit           ; Keep track of your habits
        +present         ; Emacs for presentations
        +protocol)       ; Support for org-protocol:// links
       raku              ; the artist formerly known as perl6
       php               ; perl's insecure younger brother
       ;;plantuml          ; diagrams for confusing people more
       ;;purescript        ; javascript, but functional
       python            ; beautiful is better than ugly
       ;;qt                ; the 'cutest' gui framework ever
       ;;racket            ; a DSL for DSLs
       ;;rest              ; Emacs as a REST client
       ;;ruby              ; 1.step {|i| p "Ruby is #{i.even? ? 'love' : 'life'}"}
       ;;rust              ; Fe2O3.unwrap().unwrap().unwrap().unwrap()
       ;;scala             ; java, but good
       sh                ; she sells {ba,z,fi}sh shells on the C xor
       ;;solidity          ; do you need a blockchain? No.
       ;;swift             ; who asked for emoji variables?
       ;;terra             ; Earth and Moon in alignment for performance.
       web               ; the tubes
       ;;vala              ; GObjective-C

       :email
       (mu4e +gmail)       ; WIP
       ;;notmuch             ; WIP
       ;;(wanderlust +gmail) ; WIP

       ;; Applications are complex and opinionated modules that transform Emacs
       ;; toward a specific purpose. They may have additional dependencies and
       ;; should be loaded late.
       :app
       ;;calendar
       ;;irc              ; how neckbeards socialize
       ;;(rss +org)        ; emacs as an RSS reader
       ;;twitter           ; twitter client https://twitter.com/vnought
       ;;(write            ; emacs as a word processor (latex + org + markdown)
       ;; +wordnut         ; wordnet (wn) search
       ;; +langtool)       ; a proofreader (grammar/style check) for Emacs

       :config
       ;; For literate config users. This will tangle+compile a config.org
       ;; literate config in your `doom-private-dir' whenever it changes.
       ;;literate

       ;; The default module sets reasonable defaults for Emacs. It also
       ;; provides a Spacemacs-inspired keybinding scheme and a smartparens
       ;; config. Use it as a reference for your own modules.
       (default +bindings +smartparens))

(setq evil-want-C-u-scroll t)
(doom-themes-neotree-config)

(use-package-hook! doom-themes
  :pre-init
  (setq doom-theme 'justf-tomorrow-night)
  nil)
(after! doom-themes
  (setq doom-font (font-spec :family "Hack" :size 16)
        doom-big-font (font-spec :family "Hack" :size 20)
        display-line-numbers-type nil
        global-visual-line-mode t
        visual-line-fringe-indicators '(left-curly-arrow right-curly-arrow)
        overflow-newline-into-fringe nil)

  (fringe-mode 14)
  (global-visual-line-mode +1)

  ;; FIXME: It doesn't work
  ;; Increase font when VGA monitor connected
  (if (mapc (lambda (monitor)
            (when (string-equal "VGA1" (cdr (assq 'name monitor))) t))
              (display-monitor-attributes-list))
      (doom-big-font-mode +1))
  )


(use-package-hook! evil-escape
  :pre-init
  (setq evil-escape-excluded-states '(normal)
        evil-escape-excluded-major-modes '(neotree-mode treemacs-mode term-mode vterm-mode)
        evil-escape-key-sequence "df"
        evil-escape-delay 0.25)
  (evil-define-key* '(operator insert replace visual) 'global "\C-g" #'evil-escape)
  nil)
(use-package-hook! evil-escape
  :pre-config
  (evil-escape-mode +1)
  nil)

(use-package! expand-region
  :commands (er/contract-region er/mark-symbol er/mark-word)
  :config
  (defun doom*quit-expand-region ()
    "Properly abort an expand-region region."
    (when (memq last-command '(er/expand-region er/contract-region))
      (er/contract-region 0)))
  (advice-add #'evil-escape :before #'doom*quit-expand-region)
  (advice-add #'doom/escape :before #'doom*quit-expand-region))

(after! evil
  (setq evil-move-cursor-back nil))

(after! deft
  (setq deft-directory "/home/justf/org"))

(after! popup
  (set-popup-rule! "^\\*Customize" :slot 2 :side 'right :size 0.5 :select t :quit t))

(after! org-bullets
  (setq org-bullets-bullet-list '("" "" "" "" "")))

(after! ranger
  (setq ranger-show-hidden t))

(use-package-hook! web-mode
  :post-config
    (setq-default web-mode-comment-formats
                '(("java"       . "/*")
                  ("javascript" . "//")
                  ("php"        . "//")))

    (setq web-mode-markup-indent-offset 2
          web-mode-css-indent-offset 2
          web-mode-code-indent-offset 2
          web-mode-part-padding nil
          web-mode-script-padding nil
          web-mode-style-padding nil))

(use-package-hook! php-mode
  :post-config (setq c-basic-offset 4))
;; (after! sh-script
;;   (set-company-backend! 'sh-mode
;;     '(company-shell :with company-yasnippet)))

(use-package-hook! mu4e
  :post-config
    (setq mu4e-headers-fields '((:human-date . 12)
                                (:flags . 4)
                                (:from-or-to . 25)
                                (:subject))
          shr-use-colors nil)
    (set-email-account! "gmail"
    '((mu4e-sent-folder       . "/sent")
      (mu4e-drafts-folder     . "/drafts")
      (mu4e-trash-folder      . "/trash")
      (smtpmail-smtp-user     . "justfdot@gmail.com")
      (user-mail-address      . "justfdot@gmail.com")
      (mu4e-compose-signature . "---\nIvan Filatov"))
    t))

(use-package-hook! doom-modeline
  :post-config
  (doom-modeline-def-modeline 'main
    '(bar matches buffer-info remote-host buffer-position selection-info)
    '(misc-info persp-name debug input-method buffer-encoding lsp major-mode process vcs checker " "))

  (setq doom-modeline-icon t
        doom-modeline-persp-name t
        doom-modeline-persp-name-icon t
        doom-modeline-buffer-modification-icon nil
        doom-modeline-buffer-file-name-style 'truncate-upto-project))
