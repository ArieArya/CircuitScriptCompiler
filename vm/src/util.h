#pragma once

#include <string>

#include <fmt/base.h>
#include <fmt/ranges.h>

namespace util {

inline std::string read_file(std::string_view file_name) {
    std::string contents;

    FILE* fp = fopen(file_name.data(), "rb");
    if (!fp) {
        fmt::println("read_file() error: file pointer is null");
        std::abort();
    }

    fseek(fp, 0, SEEK_END);
    size_t size = ftell(fp);
    contents.resize(size);
    rewind(fp);
    fread(&contents[0], 1, size, fp);
    fclose(fp);
    return contents;
}

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
