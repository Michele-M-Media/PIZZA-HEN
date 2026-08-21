#pragma once

#include <cstdint>
#include <string>

void pizzahen_configure_debug_services_route(uint32_t system_version);
bool pizzahen_debug_services_uses_old_route(void);
const char *pizzahen_debug_services_uri(void);
const char *pizzahen_debug_services_uri_simple(void);
std::string pizzahen_rewrite_debug_services_route(const std::string &uri);
