# Contributing

Thanks for your interest in this project. Contributions, bug reports and
ideas are welcome.

## Set up

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the project

```bash
python train.py     # train both models, compare them, save the best one
python predict.py   # predict the hand-drawn digit grid in predict.py
```

## Run the tests

```bash
pip install pytest
python -m pytest tests/
```

Please make sure the tests pass before suggesting a change.

## Suggesting a change

- **Found a bug or have an idea?** Open an issue first and describe it
  in simple words: what you expected, what actually happened.
- **Want to code it yourself?** Fork the repo, make your change on a
  new branch, and open a pull request. Explain in the PR what you
  changed and why.

## House rules

- Keep the code simple: clear names, short comments, no clever tricks.
  Someone should be able to read a file once and explain what it does.
- Do not change the reported results in the README unless you re-ran
  the training and can show the new output.
- Keep pull requests small and focused on one change.
