#pragma once
#include <string>

bool pizzahen_scan_plugin_catalog();
bool pizzahen_stop_plugin(const std::string &path, const std::string &title_id, bool is_payload);
bool pizzahen_set_plugin_autostart(const std::string &path, bool enabled);
bool pizzahen_stop_all_managed_plugins();
