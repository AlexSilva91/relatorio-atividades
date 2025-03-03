# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.

# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
setenv VIRTUAL_ENV '/home/alex/projetos_python/meta_tecnicos['
=======
setenv VIRTUAL_ENV /home/alex/projetos_python/relatorio_atividades
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/"bin":$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
<<<<<<< HEAD
    set prompt = '(meta_tecnicos[) '"$prompt"
    setenv VIRTUAL_ENV_PROMPT '(meta_tecnicos[) '
=======
    set prompt = '(relatorio_atividades) '"$prompt"
    setenv VIRTUAL_ENV_PROMPT '(relatorio_atividades) '
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c
endif

alias pydoc python -m pydoc

rehash
