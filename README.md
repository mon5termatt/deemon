<img src="deemon/assets/images/deemon.png" alt="deemon" width="300">

## Development setup

### Prerequisites

- Python `>= 3.8`

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Initialize local app data

```bash
deemon --init
```

This creates the local configuration/database used by the CLI.

## Run locally

```bash
deemon --help
deemon monitor
```

For command-specific help:

```bash
deemon monitor -h
```

## Testing / sanity checks

```bash
deemon test -h
deemon test -E '<URL regex pattern>'
deemon test -e
```

`deemon test` is intended to exercise exclusion/test logic (and optionally send a test notification using your local config).

## Documentation

- CLI help: `deemon <command> -h`
- Additional docs shipped in-repo under `docs/docs/`

## Contributing

Open an issue for bugs/feature requests and submit PRs with a short test plan.

