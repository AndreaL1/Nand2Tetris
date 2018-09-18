import argparse

from Code import *
from Exceptions import *
from Parser import *
from SymbolTable import SymbolTable


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path')
    args = parser.parse_args()
    return args.input_file_path


def main():
    input_file_path = parse_arguments()
    output_file_path = input_file_path[: input_file_path.find('.')] + '.hack'
    symbolTable = SymbolTable()
    parser = Parser(input_file_path, symbolTable)
    parser.add_labels_to_symbol_table()
    with open(output_file_path, "w") as f:
        while parser.has_more_instructions():
            parser.advance()
            code = Code(parser.instruction_type(), parser.get_instruction_fields())
            try:
                machine_instruction = code.convert_instruction_to_machine_code()
                f.write(machine_instruction)
                f.write('\n')
            except InstructionError as e:
                print(str(e) + ' ' + parser.get_instruction())


if __name__ == '__main__':
    main()

