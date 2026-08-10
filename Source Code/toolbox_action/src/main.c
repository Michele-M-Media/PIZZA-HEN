#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <unistd.h>

#define CRIT_IPC_SOC "/system_tmp/etaHEN_crit_service"
#define STATUS_FILE "/data/PIZZA_HEN/runtime/toolbox_action_status.txt"
#define DAEMON_BUFF_MAX 0x1000
#define BREW_ENABLE_TOOLBOX 0x09000011

struct IPCMessage {
    int magic;
    int cmd;
    int error;
    char msg[DAEMON_BUFF_MAX];
};

static void write_status(const char *s) {
    mkdir("/data/PIZZA_HEN", 0777);
    mkdir("/data/PIZZA_HEN/runtime", 0777);
    int fd = open(STATUS_FILE, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (fd < 0) return;
    write(fd, s, strlen(s));
    write(fd, "\n", 1);
    fsync(fd);
    close(fd);
}

int main(void) {
    unlink(STATUS_FILE);

    int fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd < 0) {
        write_status("fail:socket");
        return 2;
    }

    struct sockaddr_un server;
    memset(&server, 0, sizeof(server));
    server.sun_family = AF_UNIX;
    strncpy(server.sun_path, CRIT_IPC_SOC, sizeof(server.sun_path) - 1);

    if (connect(fd, (struct sockaddr *)&server, SUN_LEN(&server)) != 0) {
        close(fd);
        write_status("fail:daemon-offline");
        return 3;
    }

    struct IPCMessage msg;
    memset(&msg, 0, sizeof(msg));
    msg.magic = (int)0xDEADBABE;
    msg.cmd = BREW_ENABLE_TOOLBOX;
    snprintf(msg.msg, sizeof(msg.msg), "{ \"titleId\": \"PZHN00001\" }");

    if (send(fd, &msg, sizeof(msg), MSG_NOSIGNAL) < 0) {
        close(fd);
        write_status("fail:send");
        return 4;
    }
    if (recv(fd, &msg, sizeof(msg), MSG_NOSIGNAL) <= 0) {
        close(fd);
        write_status("fail:recv");
        return 5;
    }
    close(fd);

    if (msg.error != 0) {
        write_status("fail:toolbox");
        return 6;
    }

    write_status("ok");
    return 0;
}
