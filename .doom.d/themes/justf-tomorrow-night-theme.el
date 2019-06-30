;;; justf-tomorrow-night-theme.el
(require 'doom-themes)

(defgroup justf-tomorrow-night-theme nil
  "Options for doom-themes"
  :group 'doom-themes)

(defcustom justf-tomorrow-night-padded-modeline doom-themes-padded-modeline
  "If non-nil, adds a 4px padding to the mode-line. Can be an integer to
determine the exact padding."
  :group 'justf-tomorrow-night-theme
  :type '(or integer boolean))

(def-doom-theme justf-tomorrow-night
  "A theme based off of Chris Kempson's Tomorrow Dark."

  ;; name        gui       256       16
  ((bg         '("#1d1f21" nil       nil          ))
   (bg-alt     '("#161719" nil       nil          ))
   (base0      '("#0d0d0d" "black"   "black"      ))
   (base1      '("#1b1b1b" "#1b1b1b"              ))
   (base2      '("#212122" "#1e1e1e"              ))
   (base3      '("#292b2b" "#292929" "brightblack"))
   (base4      '("#3f4040" "#3f3f3f" "brightblack"))
   (base5      '("#5c5e5e" "#525252" "brightblack"))
   (base6      '("#757878" "#6b6b6b" "brightblack"))
   (base7      '("#969896" "#979797" "brightblack"))
   (base8      '("#ffffff" "#ffffff" "white"      ))
   (fg         '("#c5c8c6" "#c5c5c5" "white"))
   (fg-alt     (doom-darken fg 0.6))

   (grey       '("#5a5b5a" "#5a5a5a" "brightblack"))
   (red        '("#cc6666" "#cc6666" "red"))
   (orange     '("#de935f" "#dd9955" "brightred"))
   (yellow     '("#f0c674" "#f0c674" "yellow"))
   (dark-yellow (doom-darken yellow 0.2))
   (green      '("#b5bd68" "#b5bd68" "green"))
   (blue       '("#81a2be" "#88aabb" "brightblue"))
   (dark-blue  '("#41728e" "#41728e" "blue"))
   (teal       blue) ; FIXME replace with real teal
   (magenta    '("#c9b4cf" "#c9b4cf" "magenta"))
   (violet     '("#b294bb" "#b294bb" "brightmagenta"))
   (cyan       '("#8abeb7" "#8abeb7" "cyan"))
   (dark-cyan  (doom-darken cyan 0.4))

   ;; face categories
   (highlight      blue)
   (vertical-bar   `("#161616" ,@base0))
   (selection      `(,(car (doom-lighten bg 0.1)) ,@(cdr base4)))
   (builtin        blue)
   (comments       grey)
   (doc-comments   (doom-lighten grey 0.14))
   (constants      dark-yellow)
   (functions      blue)
   (keywords       violet)
   (methods        blue)
   (operators      fg)
   (type           yellow)
   (strings        green)
   (variables      red)
   (numbers        fg)
   (region         selection)
   (error          red)
   (warning        yellow)
   (success        green)
   (vc-modified    fg-alt)
   (vc-added       green)
   (vc-deleted     red)

   ;; custom categories
   (modeline-bg     `(,(doom-darken (car bg-alt) 0.3) ,@(cdr base3)))
   (modeline-bg-alt `(,(car bg) ,@(cdr base1)))
   (modeline-fg     fg)
   (modeline-fg-alt comments)
   (-modeline-pad
    (when justf-tomorrow-night-padded-modeline
      (if (integerp justf-tomorrow-night-padded-modeline)
          justf-tomorrow-night-padded-modeline
        4))))

  ;; --- faces ------------------------------
  ((doom-modeline-buffer-path               :foreground blue)
   (doom-modeline-buffer-major-mode         :foreground blue :bold bold)
   ;; (doom-modeline-buffer-minor-mode)
   (doom-modeline-buffer-file               :foreground fg)
   (doom-modeline-buffer-modified           :foreground yellow :bold bold)
   ;; (doom-modeline-project-parent-dir)
   (doom-modeline-project-dir               :foreground fg)
   (doom-modeline-project-root-dir          :foreground fg)
   ;; (doom-modeline-highlight)
   ;; (doom-modeline-panel)
   ;; (doom-modeline-debug)
   ;; (doom-modeline-info)
   ;; (doom-modeline-warning)
   ;; (doom-modeline-urgent)
   ;; (doom-modeline-unread-number)
   ;; (doom-modeline-bar)
   ;; (doom-modeline-inactive-bar)
   ;; (doom-modeline-evil-emacs-state)
   ;; (doom-modeline-evil-insert-state)
   ;; (doom-modeline-evil-motion-state)
   ;; (doom-modeline-evil-normal-state)
   ;; (doom-modeline-evil-operator-state)
   ;; (doom-modeline-evil-visual-state)
   ;; (doom-modeline-evil-replace-state)
   (doom-modeline-persp-name                :foreground blue)
   (doom-modeline-persp-buffer-not-in-persp :foreground grey)


   ((line-number &override) :foreground base4)
   ((line-number-current-line &override) :foreground fg)

   ;; rainbow-delimiters
   (rainbow-delimiters-depth-1-face :foreground violet)
   (rainbow-delimiters-depth-2-face :foreground blue)
   (rainbow-delimiters-depth-3-face :foreground orange)
   (rainbow-delimiters-depth-4-face :foreground green)
   (rainbow-delimiters-depth-5-face :foreground magenta)
   (rainbow-delimiters-depth-6-face :foreground yellow)
   (rainbow-delimiters-depth-7-face :foreground teal)

   (mode-line
    :background modeline-bg :foreground modeline-fg
    :box (if -modeline-pad `(:line-width ,-modeline-pad :color ,modeline-bg)))
   (mode-line-inactive
    :background modeline-bg-alt :foreground modeline-fg-alt
    :box (if -modeline-pad `(:line-width ,-modeline-pad :color ,modeline-bg-alt)))

   (cursor :background fg)
   (org-code :foreground dark-yellow)
   (org-quote :inherit 'font-lock-comment-face :background base3 :italic italic)
   (outline-2 :foreground fg :bold bold)
   (fringe :foreground base4 :inherit 'hl-line)
   (avy-lead-face :foreground yellow :background bg :bold bold)
   (avy-lead-face-0 :inherit 'avy-lead-face :weight 'normal :foreground (doom-darken yellow 0.2))
   (avy-lead-face-1 :inherit 'avy-lead-face :weight 'normal :foreground (doom-darken yellow 0.3))
   (avy-lead-face-2 :inherit 'avy-lead-face :weight 'normal :foreground (doom-darken yellow 0.4))
  )

  ;; --- variables --------------------------
  ;; ()
)

(provide 'justf-tomorrow-night-theme)
;;; justf-tomorrow-night-theme.el ends here
