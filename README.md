# Project name

[![Build](https://github.com/childmindresearch/styxgraph/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/childmindresearch/styxgraph/actions/workflows/test.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/childmindresearch/styxgraph/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/childmindresearch/styxgraph)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![stability-stable](https://img.shields.io/badge/stability-stable-green.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/childmindresearch/styxgraph/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://childmindresearch.github.io/styxgraph)

## Usage

```Python
from styxdefs import set_global_runner, get_global_runner
from styxgraph import GraphRunner

set_global_runner(DockerRunner())  # (Optional) Use any Styx runner like usual
set_global_runner(GraphRunner(get_global_runner()))  # Use GraphRunner middleware

# Use any Styx functions as usual
# ...

print(get_global_runner().mermaid())  # Print mermaid diagram

```
