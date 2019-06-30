local user_color='magenta'; [ $UID -eq 0 ] && user_color='red'

zle-keymap-select() {
    case $KEYMAP in
        vicmd)      echo -ne '\e[4 q' ;;  # Underline
        main|viins) echo -ne '\e[2 q' ;;  # Block
    esac
    zle reset-prompt
    zle -R
}

# Use block shape cursor for each new prompt.
zle-line-init() {
    zle -K viins # initiate `vi insert` as keymap (can be removed if `bindkey -V` has been set elsewhere)
    echo -ne "\e[2 q"
}


# Outputs current branch info in prompt format
function git_prompt_info() {
  local ref
  if [[ "$(command git config --get oh-my-zsh.hide-status 2>/dev/null)" != "1" ]]; then
    ref=$(command git symbolic-ref HEAD 2> /dev/null) || \
    ref=$(command git rev-parse --short HEAD 2> /dev/null) || return 0
    echo "$(parse_git_dirty)$ZSH_THEME_GIT_PROMPT_PREFIX${ref#refs/heads/}$ZSH_THEME_GIT_PROMPT_SUFFIX"
  fi
}

PROMPT=' %{$fg[white]%}%~%{$reset_color%} %(?,,%{${fg_bold[white]}%}[%?]%{$reset_color%} )%{$fg[$user_color]%}%#%{$reset_color%} '
RPROMPT='$(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="git:%{$reset_color%}%{$fg[blue]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg_bold[red]%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg_bold[blue]%}"
