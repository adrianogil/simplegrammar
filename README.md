# simplegrammar
Python Library for Text generation based in a simple grammar

## Deterministic expansion

Pass a seed to repeat the same generated output:

```python
from simplegrammar import SimpleGrammar

grammar = {"text": ["#name#"], "name": ["Ada", "Grace"]}
print(SimpleGrammar.parse(grammar, seed="daily"))
```

The CLI also accepts `--seed`:

```bash
python -m simplegrammar '{"text":["#name#"],"name":["Ada","Grace"]}' --seed daily
```
