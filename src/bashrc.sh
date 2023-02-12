if [ -z "$SIMPLEGRAMMAR_PYTHON_PATH" ]
then
    export SIMPLEGRAMMAR_PYTHON_PATH=$SIMPLEGRAMMAR_PATH/python
    export PYTHONPATH=$SIMPLEGRAMMAR_PYTHON_PATH:$PYTHONPATH
fi

alias simple-grammar="python3 -m simplegrammar"
