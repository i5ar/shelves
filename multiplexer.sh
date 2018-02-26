#!/bin/sh
#
# Start a terminal multiplexer session with separate windows for development.
# NOTE: Link this file to your home: `ln -s ~/venv/gerp/startsession.sh ~`.

# Check required programs
# https://stackoverflow.com/questions/592620/
command -v tmux > /dev/null 2>&1 || {
    echo 1>&2 "Requiere Tmux."; exit 1;
}
command -v chrome > /dev/null 2>&1 || {
    echo 1>&2 "Requiere Chrome."; exit 1;
}
command -v au > /dev/null 2>&1 || {
    echo 1>&2 "Requiere Aurelia."; exit 1;
}
command -v git > /dev/null 2>&1 || {
    echo 1>&2 "Requiere Git."; exit 1;
}

while getopts ":bhk" opt; do
    case $opt in
        b)  # Open browser tabs
            chrome http://127.0.0.1:8000/en/django-admin/shelves/ &
            chrome http://127.0.0.1:8000/en/api/shelves/ &
            chrome http://127.0.0.1:9000 &
            ;;
        h)
            echo "usage: sh $0 [-b] [-k]"
            exit 0;;
        k)  # Kill all sessions like `pkill -f tmux` but better
            tmux kill-session -a
            tmux kill-session
            sleep 0.5
            tmux list-sessions
            exit 0;;
        *)
            echo "usage: sh $0 [-b] [-k]"
            exit 1;;
    esac
done

# Set parameters
venv="$HOME/venv36gerp/"
back_end="$HOME/venv36gerp/gerp/"
front_end="$HOME/venv36gerp/gerp-front/"
o="--all --color --date=short"
f="%C(yellow)%h%x20%C(cyan)%cd%C(reset)%x20%an%C(green)%d%C(reset)%x20%s"
if [ ! -d "$venv" ] || [ ! -d "$back_end" ] || [ ! -d "$front_end" ]; then
    echo "One or more directories are missing."; exit 1;
fi

# Run commands
# https://stackoverflow.com/questions/15257130/
cd "$venv"
tmux new-session -d -s gerp -n back_end
sleep 0.5
tmux send-keys -t gerp:0 "source bin/activate" C-m
sleep 0.25
tmux send-keys -t gerp:0 "cd $back_end" C-m
tmux send-keys -t gerp:0 "./manage.py runserver" C-m
tmux split-window
sleep 0.5
tmux send-keys -t gerp:0 "source bin/activate" C-m
sleep 0.25
tmux send-keys -t gerp:0 "cd $back_end" C-m
tmux send-keys -t gerp:0 "git log $o -2 | cat -" C-m

tmux new-window -t gerp:1 -n front_end
sleep 0.5
tmux send-keys -t gerp:1 "cd $front_end" C-m
tmux send-keys -t gerp:1 "au run --watch" C-m
tmux split-window
sleep 0.5
tmux send-keys -t gerp:1 "cd $front_end" C-m
tmux send-keys -t gerp:1 "git log $o --pretty=format:\"$f\" -8 | cat -" C-m

tmux new-session -d -s logger -n back_end_logger
sleep 0.5
tmux send-keys -t logger:0 "source bin/activate" C-m
sleep 0.25
tmux send-keys -t logger:0 "cd $back_end" C-m
tmux send-keys -t logger:0 "tail -f -vn +1 *.log" C-m

tmux select-window -t gerp:0

tmux attach-session -t gerp