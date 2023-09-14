sudo apt install bash-completion
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc # kubectl 명령어를 k 로 사용할 수 있도록 약어 설정
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
echo 'source ~/.bashrc' >> /etc/bash.bashrc

# 97 ~ 99 주석제거
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi