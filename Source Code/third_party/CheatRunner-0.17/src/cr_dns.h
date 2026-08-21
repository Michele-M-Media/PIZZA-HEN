#pragma once
#include <stddef.h>

/* Resolves via raw UDP to 8.8.8.8:53, bypassing system DNS entirely - works even
 * when PS5 DNS is set to 127.0.0.1. Returns 0 on success (ip_out filled), -1 on failure. */
int cr_dns_resolve(const char *hostname, char *ip_out, size_t ip_out_sz);
