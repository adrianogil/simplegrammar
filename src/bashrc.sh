if [ -z "$SIMPLEGRAMMAR_PYTHON_PATH" ]
then
    export SIMPLEGRAMMAR_PYTHON_PATH=$SIMPLEGRAMMAR_PATH/python
    export PYTHONPATH=$SIMPLEGRAMMAR_PYTHON_PATH:$PYTHONPATH
fi


function simple-grammar()
{
    target_input=$1
    if [ -z "$target_input" ]
    then
        target_input=$(f "*.json" | default-fuzzy-finder)
    fi
    python3 -m simplegrammar ${target_input}
}
