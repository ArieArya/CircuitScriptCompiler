#pragma once

#include <iostream>
#include <string>

#include <fmt/base.h>
#include <fmt/ranges.h>

namespace instruction {

enum class InstructionType {
    // Register operations.
    kLoad,
    kMove,

    // Logical operators.
    kAnd,
    kOr,
    kNot,
    kXor,

    // Other.
    kPrint,
};

inline InstructionType from_string(std::string_view instr) {
    if (instr == "LOAD") return InstructionType::kLoad;
    if (instr == "MOV") return InstructionType::kMove;
    if (instr == "AND") return InstructionType::kAnd;
    if (instr == "OR") return InstructionType::kOr;
    if (instr == "NOT") return InstructionType::kNot;
    if (instr == "XOR") return InstructionType::kXor;
    if (instr == "PRINT") return InstructionType::kPrint;

    fmt::println("instruction::from_string() error: could not parse instruction {}.", instr);
    std::abort();
}

}  // namespace instruction
