#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

int sceSystemServiceNavigateToGoHome(void);

#define PIZZA_RUNTIME_DIR "/data/PIZZA_HEN/runtime"
#define REQUEST_TMP PIZZA_RUNTIME_DIR "/shadowmount_request.tmp"
#define REQUEST_FILE PIZZA_RUNTIME_DIR "/shadowmount_request.txt"

static int valid_choice(const char *s) {
    return s && (!strcmp(s, "stable") || !strcmp(s, "experimental") || !strcmp(s, "skip"));
}

int main(int argc, char **argv) {
    const char *choice = NULL;
    if (argc > 0 && valid_choice(argv[0])) choice = argv[0];
    if (!choice && argc > 1 && valid_choice(argv[1])) choice = argv[1];
    if (!choice) return 2;

    mkdir("/data/PIZZA_HEN", 0777);
    mkdir(PIZZA_RUNTIME_DIR, 0777);

    int fd = open(REQUEST_TMP, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (fd < 0) return 3;
    size_t n = strlen(choice);
    if (write(fd, choice, n) != (ssize_t)n || write(fd, "\n", 1) != 1) {
        close(fd);
        unlink(REQUEST_TMP);
        return 4;
    }
    fsync(fd);
    close(fd);
    unlink(REQUEST_FILE);
    if (rename(REQUEST_TMP, REQUEST_FILE) != 0) {
        unlink(REQUEST_TMP);
        return 5;
    }

    /* R7.15: the selector request is now durable. Return the PS5 browser to
       Home immediately; the bootstrapper owns the remaining ShadowMount ->
       FTP -> Debug pipeline and does not depend on this browser staying open. */
    usleep(150000);
    (void)sceSystemServiceNavigateToGoHome();
    return 0;
}
