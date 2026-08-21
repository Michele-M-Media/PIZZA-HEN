/*
 * PIZZA HEN Debug Services route adapter.
 *
 * Route policy is the OnionHEN 0.0.10 policy already vendored in PIZZA HEN.
 * This wrapper mirrors Onion's shellui debug_settings_route_runtime exactly:
 * configure once from the real system version, use firmware-selected URIs,
 * and rewrite stock debug_settings deeplinks to debug_settings_old on 11.x+.
 */
#include "debug_services_route.hpp"
#include "onion_debug_settings_route_policy.hpp"

namespace {
onion::debug_settings_route::DebugSettingsRoutePolicy g_debug_services_route;
}

void pizzahen_configure_debug_services_route(uint32_t system_version) {
  g_debug_services_route =
      onion::debug_settings_route::DebugSettingsRoutePolicy::for_system_version(
          system_version);
}

bool pizzahen_debug_services_uses_old_route(void) {
  return g_debug_services_route.uses_old_route();
}

const char *pizzahen_debug_services_uri(void) {
  return g_debug_services_route.toolbox_uri(
      onion::debug_settings_route::UriKind::WithMode);
}

const char *pizzahen_debug_services_uri_simple(void) {
  return g_debug_services_route.toolbox_uri(
      onion::debug_settings_route::UriKind::Simple);
}

std::string pizzahen_rewrite_debug_services_route(const std::string &uri) {
  return g_debug_services_route.rewrite(uri);
}
