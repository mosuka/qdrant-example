# Qdrant Example

## Setup Pyenv

See [official installation documentation](https://github.com/pyenv/pyenv#installation).

## Setup Poetry

See [official installation documentation](https://python-poetry.org/docs/#installation).

## Setup Python

```shell
sudo apt update
sudo apt upgrade
sudo apt install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev
pyenv install 3.11.1
pyenv local 3.11.1
python -m venv .venv
source .venv/bin/activate
```

## Setup Project

```shell
make init
```

## Start Qdrant

```shell
docker-compose up
```

## Examples

### Add Example

```shell
python -m qdrant_example add example ./examples/docs.jsonl
```

### Query Example

```shell
python -m qdrant_example query example -f "$(cat ./examples/filter.json)" 家でできる仕事
```
