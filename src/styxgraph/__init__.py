""".. include:: ../../README.md"""  # noqa: D415

import pathlib
from typing import Generic, TypeVar

from styxdefs import (
    Execution,
    InputPathType,
    Metadata,
    OutputPathType,
    Runner,
)

T = TypeVar("T", bound=Runner)


class _GraphExecution(Execution):
    """Graph execution."""

    def __init__(
        self, base: Execution, graph_runner: "GraphRunner", metadata: Metadata
    ) -> None:
        """Create a new GraphExecution."""
        self.base = base
        self.graph_runner = graph_runner
        self.metadata = metadata
        self.input_files: list[InputPathType] = []
        self.output_files: list[OutputPathType] = []

    def input_file(self, host_file: InputPathType, resolve_parent: bool = True) -> str:
        """Resolve input file."""
        self.input_files.append(host_file)
        return self.base.input_file(host_file, resolve_parent=resolve_parent)

    def run(self, cargs: list[str]) -> None:
        """Run the command."""
        self.graph_runner.graph_append(
            self.metadata, self.input_files, self.output_files
        )
        return self.base.run(cargs)

    def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
        """Resolve output file."""
        output_file = self.base.output_file(local_file, optional)
        self.output_files.append(output_file)
        return output_file


# Define a new runner
class GraphRunner(Runner, Generic[T]):
    """Graph runner."""

    def __init__(self, base: T) -> None:
        """Create a new GraphRunner."""
        self.base: T = base
        self._graph: list[tuple[str, list[InputPathType], list[OutputPathType]]] = []

    def start_execution(self, metadata: Metadata) -> Execution:
        """Start a new execution."""
        return _GraphExecution(self.base.start_execution(metadata), self, metadata)

    def graph_append(
        self,
        metadata: Metadata,
        input_file: list[InputPathType],
        output_file: list[OutputPathType],
    ) -> None:
        """Append a node to the graph."""
        self._graph.append((metadata.name, input_file, output_file))

    def node_graph_mermaid(self) -> str:
        """Generate a mermaid graph of the graph."""
        connections: list[str] = []
        inputs_lookup: dict[str, list[str]] = {}
        outputs_lookup: dict[str, str] = {}
        for id, inputs, outputs in self._graph:
            for input in inputs:
                if input not in inputs_lookup:
                    inputs_lookup[input] = []
                inputs_lookup[input].append(id)
            root_output = outputs[0]
            outputs_lookup[str(root_output)] = id

        for id, inputs, _ in self._graph:
            for input in inputs:
                for output, output_id in outputs_lookup.items():
                    if pathlib.Path(input).is_relative_to(
                        output
                    ):  # is subfolder/file in output root
                        connections.append(f"{output_id} --> {id}")

        # Generate mermaid
        mermaid = "graph TD\n"
        for id, _, _ in self._graph:
            mermaid += f"  {id}\n"
        for connection in connections:
            mermaid += f"  {connection}\n"
        return mermaid
