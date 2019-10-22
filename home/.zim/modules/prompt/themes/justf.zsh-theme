# -*- mode: sh -*-

# Justf theme, customization of Minimal theme
# https://github.com/S1cK94/minimal
#
# Requires the `git-info` zmodule to be included in the .zimrc file.

# Global variables
function {
  ROOT_PROMPT='%F{red}#%f'
  USER_PROMPT='%F{magenta}%%%f'

  ON_COLOR='%F{green}'
  OFF_COLOR='%f'
  ERR_COLOR='%F{red}'
}

prompt_justf_host() {
  if [[ -n ${SSH_CONNECTION} ]]; then
    print -n " %F{cyan}@%m%f"
  fi
}

prompt_justf_user() {
  print -n '%(!.${ROOT_PROMPT}.${USER_PROMPT}) '
}

prompt_justf_jobs() {
  print -n '%(1j.%F{blue}jobs:%j%f .)'
}

prompt_justf_status() {
  print -n '%(0?..[%?] )'
}

prompt_justf_path() {
  print -n "%F{white}$(short_pwd) "
}

prompt_justf_git() {
  if [[ -n ${git_info} ]]; then
    print -n "${(e)git_info[prompt]}"
  fi
}

function zle-line-init zle-keymap-select {
  case $KEYMAP in
      vicmd)      echo -ne '\e[4 q' ;;  # Underline
      main|viins) echo -ne '\e[2 q' ;;  # Block
  esac
  zle reset-prompt
  zle -R
}

prompt_justf_precmd() {
  (( ${+functions[git-info]} )) && git-info
}

prompt_justf_setup() {
  zle -N zle-line-init
  zle -N zle-keymap-select

  autoload -Uz colors && colors
  autoload -Uz add-zsh-hook

  prompt_opts=(cr percent sp subst)

  add-zsh-hook precmd prompt_justf_precmd

  zstyle ':zim:git-info:branch' format '%b'
  zstyle ':zim:git-info:commit' format '%c'
  zstyle ':zim:git-info:clean' format '%F{green}'
  zstyle ':zim:git-info:dirty' format '%F{red}'
  zstyle ':zim:git-info:keys' format \
    'prompt' '%C%Dgit:%f%b%c'

  PROMPT="\$(prompt_justf_host) $(prompt_justf_path)$(prompt_justf_status)$(prompt_justf_user)"
  RPROMPT='$(prompt_justf_jobs)$(prompt_justf_git)'
}

prompt_justf_setup "$@"
