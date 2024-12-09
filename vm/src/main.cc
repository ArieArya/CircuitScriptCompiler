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

namespace {
std::string kExampleIR = R"(LOAD r1, 1
LOAD r2, 0
OR t1, r1, r2
OR t2, r1, t1
MOV w1, t2
AND t3, r1, r2
MOV w2, t3
PRINT w1
PRINT w2
NOT t4, w1
MOV w3, t4
PRINT w3)";
}

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

        fmt::println("{} := {}", args[0], args[1]);
        break;
    }
    case InstructionType::kMove: {
        assert(args.size() == 2);

        fmt::println("{} <- {}", args[0], args[1]);
        break;
    }
    case InstructionType::kAnd: {
        assert(args.size() == 3);

        fmt::println("{} <- and({}, {})", args[0], args[1], args[2]);
        break;
    }
    case InstructionType::kOr: {
        assert(args.size() == 3);

        fmt::println("{} <- or({}, {})", args[0], args[1], args[2]);
        break;
    }
    case InstructionType::kNot: {
        assert(args.size() == 2);

        fmt::println("{} <- not({})", args[0], args[1]);
        break;
    }
    default: {
        return;  // TODO: Debug use; remove this.

        fmt::println("process_instruction() error: unknown instruction");
        std::abort();
    }
    }
}

int main() {
    std::istringstream ss(kExampleIR);
    std::string line;
    while (std::getline(ss, line)) {
        auto instr_str = util::parse_first_word(line);
        auto args = util::split(line.substr(instr_str.length()));

        auto instr = instruction::from_string(instr_str);
        process_instruction(instr, args);
    }
}
