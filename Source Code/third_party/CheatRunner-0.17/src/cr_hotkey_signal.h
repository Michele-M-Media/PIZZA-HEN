#ifndef CR_HOTKEY_SIGNAL_H
#define CR_HOTKEY_SIGNAL_H

#include <stdint.h>

/* loopback signal port from the injected GetData hook, separate from
 * CHEATRUNNER_HTTP_PORT */
#define CR_HOTKEY_SIGNAL_PORT 39217

/* daemon -> injected payload, combo/hold_ms config broadcast - separate port
 * so it doesn't collide with the payload -> daemon "hotkey fired" signal above. */
#define CR_HOTKEY_CONFIG_SIGNAL_PORT 39218

typedef struct {
  uint32_t combo;
  uint32_t hold_ms;
} cr_hotkey_config_packet_t;

#endif /* CR_HOTKEY_SIGNAL_H */
