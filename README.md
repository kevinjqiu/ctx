```
________________________  ___
\_   ___ \__    ___/\   \/  /
/    \  \/ |    |    \     /
\     \____|    |    /     \
 \______  /|____|   /___/\  \
        \/                \_/
```
A simple CLI tool for keeping track of context and time

# Install

    $ go get github.com/kevinjqiu/ctx

# Usage
## Start a new context

    $ ctx start standup
    You're working on standup

## You can put a note on the context

    $ ctx title "daily standup"
    Set title for task: standup

## Show the current context

    $ ctx info
    standup             daily standup       5m        Active

## Stop time tracking on the current context

    $ ctx stop

## To list all contexts

    $ ctx list
    foo                                     Stopped
    grooming            grooming meeting    Stopped
    standup             daily standup       Active
