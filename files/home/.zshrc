# ============================================================
# Zsh + Oh-My-Zsh + Starship
# Rebuilt after The Great Cleansing of 2025
# ============================================================

# ----------------------------
# Oh-My-Zsh core
# ----------------------------
export ZSH="$HOME/.oh-my-zsh"

# Disable OMZ theme (Starship handles the prompt)
ZSH_THEME=""

# ----------------------------
# Completion behavior
# ----------------------------
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

# ----------------------------
# Plugins
# ----------------------------
plugins=(
  git
  sudo
  docker
  systemd
  command-not-found
  colored-man-pages
)

# ----------------------------
# Load Oh-My-Zsh
# ----------------------------
source "$ZSH/oh-my-zsh.sh"

# ----------------------------
# Starship prompt (MUST be after OMZ)
# ----------------------------
eval "$(starship init zsh)"

# ----------------------------
# Autosuggestions (after prompt)
# ----------------------------
if [ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
  source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# ----------------------------
# Syntax highlighting (ALWAYS LAST)
# ----------------------------
if [ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
  source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# ----------------------------
# User config / aliases go below
# ----------------------------
# alias ll='ls -lah'

clear
neofetch

# Created by `pipx` on 2025-12-15 19:17:18
export PATH="$PATH:/home/shorty/.local/bin"
