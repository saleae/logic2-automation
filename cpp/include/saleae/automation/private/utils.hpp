#ifndef SALEAE_AUTOMATION_PRIVATE_UTILS_HPP
#define SALEAE_AUTOMATION_PRIVATE_UTILS_HPP

// helper type for the visitor #4
template <class... Ts>
struct overloaded : Ts... { using Ts::operator()...; };
// explicit deduction guide (not needed as of C++20)
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

#endif // SALEAE_AUTOMATION_PRIVATE_UTILS_HPP
