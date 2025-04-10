# llm-xai
LLM plugin to access xAI's models

[![PyPI](https://img.shields.io/pypi/v/llm-xai.svg)](https://pypi.org/project/llm-xai/0.2/)
[![Changelog](https://img.shields.io/github/v/release/ghostofpokemon/llm-xai?include_prereleases&label=changelog)](https://github.com/ghostofpokemon/llm-xai/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ghostofpokemon/llm-xai/blob/main/LICENSE)
[LLM](https://llm.datasette.io/) plugin for models hosted by [xAI](https://x.ai/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-xai
```

## Configuration

You will need an API key from xAI. You can [obtain one here](https://console.x.ai).

You can set that as an environment variable called `XAI_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set xai
```
```
Enter key: <paste key here>
```

## Usage

To list available models, run:
```bash
llm models list
```
You should see a list that looks something like this:
```
xAI: xAI/grok-beta
xAI: xAIcompletion/grok-beta
...
```
To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm chat -m xAI/grok-beta
```
Enter your prompt, and have a chat:
```shell
Chatting with xAI/grok-beta
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
> sup playa
Hey, what's up?
>
```

xAI offers a completion endpoint.
```bash
llm -m xAIcompletion/grok-beta "You must know this about me:"
```
```shell
 I’m not a fan of being alone. I have a hard time finding peace in the silence. My own thoughts drive me crazy. But I knew I had to do this for myself. I had to prove to myself that I could be alone and be okay with it
...
```

## Reasoning Feature

The xAI models `grok-3-mini-beta` and `grok-3-mini-fast-beta` support a `reasoning_effort` parameter that shows the model's internal reasoning process alongside its final response. Note that `grok-3-beta` and `grok-3-fast-beta` do not support reasoning.

### Usage

```bash
llm -m xAI/grok-3-mini-beta "What is 101*3?" -o reasoning_effort high
```

To disable streaming:

```bash
llm -m xAI/grok-3-mini-beta "What is 101*3?" -o reasoning_effort high --no-stream
```

Available options:
- `high`: More detailed reasoning
- `low`: Quick, less detailed reasoning

Works with both chat and completion models.

You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set grok xAI/grok-beta
```
Now you can prompt Claude using:
```bash
cat llm_xai.py | llm -m grok-beta -s 'write some pytest tests for this'
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-xai
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
