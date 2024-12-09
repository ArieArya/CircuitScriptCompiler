#pragma once

#include <string>

namespace util {

inline std::string parse_first_word(std::string_view str) {
    std::string result;
    for (char ch : str) {
        if (ch == ' ') break;
        else result += ch;
    }
    return result;
}

// Skips all whitespace.
inline std::vector<std::string> split(std::string_view str) {
    std::vector<std::string> result;

    std::string s;
    for (char ch : str) {
        if (ch == ' ') {
            continue;
        } else if (ch == ',') {
            result.emplace_back(s);
            s.clear();
        } else {
            s += ch;
        }
    }
    if (!s.empty()) {
        result.emplace_back(s);
    }

    return result;
}

}  // namespace util
