#include <cassert>
#include <iostream>
#include <sstream>
#include <unordered_map>
#include <vector>

#include <fmt/base.h>
#include <fmt/ranges.h>

#include "instruction.h"
#include "util.h"

using namespace instruction;

// TODO: Clean this up! This is a *very* quick and dirty prototype.
std::unordered_map<std::string, bool> symbol_table;

bool get_argument_value(const std::string& arg) {
    if (arg == "0") return false;
    if (arg == "1") return true;

    return symbol_table[arg];
}

void process_instruction(InstructionType instr_type, const std::vector<std::string>& args) {
    switch (instr_type) {
    case InstructionType::kLoad: {
        assert(args.size() == 2);

        bool val = get_argument_value(args[1]);
        symbol_table[args[0]] = val;
        break;
    }
    case InstructionType::kMove: {
        assert(args.size() == 2);

        bool val = get_argument_value(args[1]);
        symbol_table[args[0]] = val;
        break;
    }
    case InstructionType::kAnd: {
        assert(args.size() == 3);

        bool val1 = get_argument_value(args[1]);
        bool val2 = get_argument_value(args[2]);
        symbol_table[args[0]] = val1 && val2;
        break;
    }
    case InstructionType::kOr: {
        assert(args.size() == 3);

        bool val1 = get_argument_value(args[1]);
        bool val2 = get_argument_value(args[2]);
        symbol_table[args[0]] = val1 || val2;
        break;
    }
    case InstructionType::kNot: {
        assert(args.size() == 2);

        bool val = get_argument_value(args[1]);
        symbol_table[args[0]] = !val;
        break;
    }
    case InstructionType::kPrint: {
        assert(args.size() == 1);

        bool val = get_argument_value(args[0]);
        fmt::println("{}", val);
        break;
    }
    default: {
        return;  // TODO: Debug use; remove this.

        fmt::println("process_instruction() error: unknown instruction");
        std::abort();
    }
    }
}

int main(int argc, char* argv[]) {
    std::string file_str = util::read_file(argv[1]);

    std::istringstream ss(file_str);
    std::string line;
    while (std::getline(ss, line)) {
        auto instr_str = util::parse_first_word(line);
        auto args = util::split(line.substr(instr_str.length()));

        auto instr = instruction::from_string(instr_str);
        process_instruction(instr, args);
    }

    // TODO: Debug use; remove this.
    fmt::println("{}", symbol_table);
}
