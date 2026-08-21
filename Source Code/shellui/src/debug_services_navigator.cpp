/*
 * PIZZA HEN — OnionHEN 0.0.10 Debug Settings navigator port.
 *
 * Source behavior preserved:
 *   debug_settings     -> RN DebugSettingsScreen
 *   debug_settings_old -> DebugSettingsOldScreen -> Legacy SettingPage -> XML
 *
 * UpdateNavigationState and DebugSettingsModule.GetModel are both observed
 * because opening Debug Settings from inside Settings can bypass BootHelper.
 */
#include "HookedFuncs.hpp"
#include "debug_services_route.hpp"
#include "hook_lifecycle.hpp"

#include <chrono>
#include <string>

void (*ReactNavigatorManager_UpdateNavigationState_Orig)(MonoObject*, MonoObject*) = nullptr;
void (*DebugSettings_GetModel_Orig)(MonoObject*, MonoObject*, MonoObject*) = nullptr;

namespace {
static constexpr auto kLegacyNavDebounce = std::chrono::milliseconds(750);
static std::chrono::steady_clock::time_point g_last_legacy_nav{};

static std::string MonoObjectToString(MonoObject *obj) {
  if (!obj || !mono_object_get_class)
    return "";
  MonoClass *klass = mono_object_get_class(obj);
  if (!klass)
    return "";
  MonoString *text = Invoke<MonoString *>(nullptr, klass, obj, "ToString");
  return text ? Mono_to_String(text) : "";
}

static bool within_legacy_nav_debounce() {
  const auto now = std::chrono::steady_clock::now();
  if (g_last_legacy_nav.time_since_epoch().count() != 0 &&
      (now - g_last_legacy_nav) < kLegacyNavDebounce)
    return true;
  g_last_legacy_nav = now;
  return false;
}

static void clear_legacy_nav_debounce(const char *why) {
  g_last_legacy_nav = {};
#if SHELL_DEBUG == 1
  shellui_log("PIZZA HEN Onion nav debounce cleared (%s)", why ? why : "unknown");
#else
  (void)why;
#endif
}

static void navigate_legacy_debug_settings(const char *reason) {
  (void)reason;
  if (within_legacy_nav_debounce()) {
#if SHELL_DEBUG == 1
    shellui_log("PIZZA HEN Onion nav debounce skip (%s)", reason ? reason : "unknown");
#endif
    return;
  }

  MonoDomain *dom = mono_domain_get ? mono_domain_get() : nullptr;
  if (!dom)
    dom = Root_Domain;

  if (!dom || !mono_string_new) {
    GoToURI(pizzahen_debug_services_uri_simple());
    return;
  }

  MonoString *uri = mono_string_new(dom, pizzahen_debug_services_uri_simple());
  if (!uri) {
    GoToURI(pizzahen_debug_services_uri_simple());
    return;
  }

  if (boot_orig) {
    const bool ok = boot_orig(uri, 0, nullptr);
#if SHELL_DEBUG == 1
    shellui_log("PIZZA HEN Onion BootHelper.Boot(3) legacy (%s) ret=%d",
                reason ? reason : "unknown", ok ? 1 : 0);
#endif
    if (!ok)
      clear_legacy_nav_debounce("Boot(3) failed");
    return;
  }

  if (boot_orig_2) {
    const bool ok = boot_orig_2(uri, 0);
#if SHELL_DEBUG == 1
    shellui_log("PIZZA HEN Onion BootHelper.Boot(2) legacy (%s) ret=%d",
                reason ? reason : "unknown", ok ? 1 : 0);
#endif
    if (!ok)
      clear_legacy_nav_debounce("Boot(2) failed");
    return;
  }

  GoToURI(pizzahen_debug_services_uri_simple());
}
} // namespace

void ReactNavigatorManager_UpdateNavigationState_Hook(MonoObject *instance,
                                                       MonoObject *state) {
  if (!shellui_hooks_are_ready()) {
    if (ReactNavigatorManager_UpdateNavigationState_Orig)
      ReactNavigatorManager_UpdateNavigationState_Orig(instance, state);
    return;
  }

  if (!pizzahen_debug_services_uses_old_route()) {
    if (ReactNavigatorManager_UpdateNavigationState_Orig)
      ReactNavigatorManager_UpdateNavigationState_Orig(instance, state);
    return;
  }

  const std::string state_text = MonoObjectToString(state);

  if (state_text.find("ps5:settings:main") != std::string::npos ||
      state_text.find("CategoriesScreen") != std::string::npos) {
    if (g_last_legacy_nav.time_since_epoch().count() != 0)
      clear_legacy_nav_debounce("settings main/categories");
  }

  if (state_text.find("DebugSettingsScreen") != std::string::npos &&
      state_text.find("DebugSettingsOldScreen") == std::string::npos &&
      state_text.find("ps5:settings:debug settings old") == std::string::npos) {
#if SHELL_DEBUG == 1
    shellui_log("PIZZA HEN Onion: block RN DebugSettingsScreen -> legacy host");
#endif
    navigate_legacy_debug_settings("UpdateNavigationState");
    return;
  }

  if (ReactNavigatorManager_UpdateNavigationState_Orig)
    ReactNavigatorManager_UpdateNavigationState_Orig(instance, state);
}

void DebugSettings_GetModel_Hook(MonoObject *instance, MonoObject *param,
                                 MonoObject *promise) {
  if (!shellui_hooks_are_ready()) {
    if (DebugSettings_GetModel_Orig)
      DebugSettings_GetModel_Orig(instance, param, promise);
    return;
  }

  if (!pizzahen_debug_services_uses_old_route()) {
    if (DebugSettings_GetModel_Orig)
      DebugSettings_GetModel_Orig(instance, param, promise);
    return;
  }

  std::string param_text;
  std::string page_id;

  if (param && mono_object_get_class) {
    MonoClass *param_class = mono_object_get_class(param);
    if (param_class) {
      MonoDomain *dom = mono_domain_get ? mono_domain_get() : nullptr;
      if (!dom)
        dom = Root_Domain;
      MonoString *page_key =
          (dom && mono_string_new) ? mono_string_new(dom, "pageId") : nullptr;

      if (page_key) {
        MonoObject *page_token = Invoke<MonoObject *>(
            nullptr, param_class, param, "GetValue", page_key);
        if (page_token) {
          MonoClass *token_class = mono_object_get_class(page_token);
          if (token_class) {
            MonoString *page_string = Invoke<MonoString *>(
                nullptr, token_class, page_token, "ToString");
            if (page_string)
              page_id = Mono_to_String(page_string);
          }
        }
      }

      MonoString *param_string =
          Invoke<MonoString *>(nullptr, param_class, param, "ToString");
      if (param_string)
        param_text = Mono_to_String(param_string);
    }
  }

  if (page_id == "id_debug_settings" ||
      param_text.find("id_debug_settings") != std::string::npos) {
#if SHELL_DEBUG == 1
    shellui_log("PIZZA HEN Onion: DebugSettings.GetModel -> legacy host");
#endif
    navigate_legacy_debug_settings("GetModel");
    return;
  }

  if (DebugSettings_GetModel_Orig)
    DebugSettings_GetModel_Orig(instance, param, promise);
}
