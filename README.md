# Score-lit

This is a play app created to track my sheet music library using [streamlit][streamlit-io].

## Developer setup

```bash
$ git clone git@github.com:keiranmraine/score-lit.git
$ cd score-lit
$ git hf init # optional, see https://github.com/datasift/gitflow
$ python -m venv .venv
# windows-bash
$ . .venv/Scripts/activate
# linux/mac
$ source .venv/bin/activate
$ pip install streamlit plotly-express
$ streamlit run score.py
```

<!-- references -->
[streamlit-io]: https://streamlit.io/