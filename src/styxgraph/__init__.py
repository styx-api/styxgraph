""".. include:: ../../README.md"""  # noqa: D415

import pathlib
from styxdefs import set_global_runner, get_global_runner, Runner, Execution, Metadata, InputPathType, OutputPathType


class _GraphExecution(Execution):
    def __init__(self, base: Execution, graph_runner: 'GraphRunner', metadata: Metadata) -> None:
        self.base = base
        self.graph_runner = graph_runner
        self.metadata = metadata
        self.input_files = []
        self.output_files = []

    def input_file(self, host_file: InputPathType) -> str:
        self.input_files.append(host_file)
        return self.base.input_file(host_file)

    def run(self, cargs: list[str]) -> None:
        self.graph_runner.graph_append(self.metadata, self.input_files, self.output_files)
        return self.base.run(cargs)

    def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
        output_file = self.base.output_file(local_file, optional)
        self.output_files.append(output_file)
        return output_file


# Define a new runner
class GraphRunner(Runner):
    def __init__(self, base: Runner):
        self.base = base
        self.graph: list[tuple[str, list[InputPathType], list[OutputPathType]]] = []

    def start_execution(self, metadata: Metadata) -> Execution:
        return _GraphExecution(self.base.start_execution(metadata), self, metadata)
    
    def graph_append(self, metadata: Metadata, input_file: list[InputPathType], output_file: list[OutputPathType]) -> None:
        print(f'Appending {metadata.name} with {input_file} and {output_file}')
        self.graph.append((metadata.name, input_file, output_file))

    def mermaid(self) -> str:
        connections = []
        inputs_lookup = {}
        outputs_lookup = {}
        for id, inputs, outputs in self.graph:
            for input in inputs:
                if input not in inputs_lookup:
                    inputs_lookup[input] = []
                inputs_lookup[input].append(id)
            root_output = outputs[0]
            outputs_lookup[root_output] = id

        for id, inputs, _ in self.graph:
            for input in inputs:
                for output, output_id in outputs_lookup.items():
                    if pathlib.Path(input).is_relative_to(output):  # is subfolder/file in output root
                        connections.append(f'{output_id} --> {id}')
        
        # Generate mermaid
        mermaid = 'graph TD\n'
        for id, _, _ in self.graph:
            mermaid += f'  {id}\n'
        for connection in connections:
            mermaid += f'  {connection}\n'
        return mermaid
