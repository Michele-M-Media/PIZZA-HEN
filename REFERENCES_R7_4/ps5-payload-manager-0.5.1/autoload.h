#pragma once

/* 
 * Start the autoload sequence in a background thread.
 * Returns 0 on success, -1 on failure.
 */
int pldmgr_autoload_start();
void pldmgr_autoload_abort();
void pldmgr_autoload_reset();
int pldmgr_autoload_get_remaining_seconds();
long long pldmgr_autoload_get_remaining_ms();
void pldmgr_autoload_get_status(int *total, int *done, char *current);
void pldmgr_autoload_update_config_entry(const char *old_filename, const char *new_filename);
