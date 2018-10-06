uthor: thinkycx
# date: 2018-04-30
# usage: install zsh for one script

# get this script, you may need to run:
# apt-get update && apt-get install curl -y  
# curl raw URL > thinkycx-zsh.sh
# bash thinkycx-zsh.sh

apt-get install sudo -y
sudo apt-get update -y
sudo apt-get install git -y
sudo apt-get install git -y # for not install strange bug 20180831
sudo apt-get install curl -y 
sudo apt-get install zsh -y
#optional
#sudo apt-get install terminator -y 
sudo apt-get install vim -y 
sudo apt-get install python-pip -y
# https://github.com/robbyrussell/oh-my-zsh
# git config --global --unset http.proxy 
# git config --global --unset https.proxy

# 终端配置（弃用）
# http://www.cnblogs.com/yangshiyu/p/6941555.html
# preferences font ubuntu mono13
# local ret_status="%(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ )"
# PROMPT='${ret_status}%{$fg[cyan]%}%~%{$reset_color%}$(git_prompt_info)%{$fg[green]%}$ %{$fg[white]%}'

# ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}(%{$fg[red]%}"
# ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
# ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%})"
#ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"

# need to exit manually
echo "[!] ENTER exit manually!"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"


bash_aliases=$(cat ~/.zshrc | grep "~/.bash_aliases")
if [ -z "$bash_aliases" ];then
  echo "[*] add ~/.bash_aliases in ~/.zshrc"
cat <<EOF  >>~/.zshrc

# add ~/.bash_aliases 
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
EOF
else
  echo "[*] ~/.bash_aliases exists in ~/.zshrc"
fi

# use dircolors
echo "[*] add ~/.dircolors in ~/.zshrc"
dircolors -p > ~/.dircolors
cat <<EOF  >>~/.zshrc

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
EOF

# install zsh-autosuggestions
if [ ! -d "$HOME/.zsh/zsh-autosuggestions" ]; then
  git clone git://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
  echo "source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc 
else
  echo "[*] ~/.zsh/zsh-autosuggestions exists..."
fi

# install zsh-syntax-highlighting
if [ ! -d "$HOME/.zsh/zsh-syntax-highlighting" ]; then
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
  echo "source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
else
  echo "[*] ~/.zsh/zsh-syntax-highlighting exists...."
fi

sudo apt-get install autojump -y
echo "[!] need to add autojump in ~/.zshrc plugin and logoff manually!"


# change zsh to default shell
sudo chsh -s /bin/zsh
echo "[*] ENJOY!"

/bin/zsh


# uninstall
# rm -rf ~/.oh-my-zsh
