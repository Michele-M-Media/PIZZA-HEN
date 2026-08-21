#ifndef SHA256_H
#define SHA256_H

#include <stddef.h>

typedef struct SHA256_CTX {
    unsigned char data[64];
    unsigned int datalen;
    unsigned long long bitlen;
    unsigned int state[8];
} SHA256_CTX;

void sha256_init(SHA256_CTX *ctx);
void sha256_update(SHA256_CTX *ctx, const unsigned char data[], size_t len);
void sha256_final(SHA256_CTX *ctx, unsigned char hash[]);

/* Compute SHA256 of a file, writing the 64-char hex string to out_hex.
 * Returns 0 on success, -1 on failure. */
int compute_sha256_file(const char *path, char out_hex[65]);

#endif
