/*
 gcc read_taskstats.c `pkg-config --cflags --libs libnl-3.0 libnl-genl-3.0` -o read_taskstats
*/
#include <stdlib.h>
#include <linux/taskstats.h>
#include <netlink/netlink.h>
#include <netlink/genl/genl.h>
#include <netlink/genl/ctrl.h>

void usage(int argc, char *argv[]);
int msg_recv_cb(struct nl_msg *, void *);

int main(int argc, char *argv[])
{
    struct nl_sock *sock;
    struct nl_msg *msg;
    int family;
    int pid = -1;
    char *cpumask;

    if (argc > 2 && strcmp(argv[1], "--pid") == 0) {
        pid = atoi(argv[2]);
    } else if (argc > 2 && strcmp(argv[1], "--cpumask") == 0) {
        cpumask = argv[2];
    } else {
        usage(argc, argv);
        exit(1);
    }

    sock = nl_socket_alloc();

    // Connect to generic netlink socket on kernel side
    genl_connect(sock);

    // get the id for the TASKSTATS generic family
    family = genl_ctrl_resolve(sock, "TASKSTATS");

    // register for task exit events
    msg = nlmsg_alloc();

    genlmsg_put(msg, NL_AUTO_PID, NL_AUTO_SEQ, family, 0, NLM_F_REQUEST,
            TASKSTATS_CMD_GET, TASKSTATS_VERSION);
    if (pid > 0) {
        nla_put_u32(msg, TASKSTATS_CMD_ATTR_PID, pid);
    } else {
        nla_put_string(msg, TASKSTATS_CMD_ATTR_REGISTER_CPUMASK,
                   cpumask);
    }
    nl_send_auto_complete(sock, msg);
    nlmsg_free(msg);

    // specify a callback for inbound messages
    nl_socket_modify_cb(sock, NL_CB_MSG_IN, NL_CB_CUSTOM, msg_recv_cb,
                NULL);
    if (pid > 0) {
        nl_recvmsgs_default(sock);
    } else {
        while (1)
            nl_recvmsgs_default(sock);
    }
    return 0;
}

void usage(int argc, char *argv[])
{
    printf("USAGE: %s option\nOptions:\n"
           "\t--pid pid : get statistics during a task's lifetime.\n"
           "\t--cpumask mask : obtain statistics for tasks which are exiting. \n"
           "\t\tThe cpumask is specified as an ascii string of comma-separated \n"
           "\t\tcpu ranges e.g. to listen to exit data from cpus 1,2,3,5,7,8\n"
           "\t\tthe cpumask would be '1-3,5,7-8'.\n", argv[0]);
}

#define printllu(str, value)    printf("%s: %llu\n", str, value)

int msg_recv_cb(struct nl_msg *nlmsg, void *arg)
{
    struct nlmsghdr *nlhdr;
    struct nlattr *nlattrs[TASKSTATS_TYPE_MAX + 1];
    struct nlattr *nlattr;
    struct taskstats *stats;
    int rem;

    nlhdr = nlmsg_hdr(nlmsg);

    // validate message and parse attributes
    genlmsg_parse(nlhdr, 0, nlattrs, TASKSTATS_TYPE_MAX, 0);

    if (nlattr = nlattrs[TASKSTATS_TYPE_AGGR_PID]) {
        stats = nla_data(nla_next(nla_data(nlattr), &rem));

        printf("---\n");
        printf("pid: %u\n", stats->ac_pid);
        printf("command: %s\n", stats->ac_comm);
        printf("status: %u\n", stats->ac_exitcode);
        printf("time:\n");
        printf("  start: %u\n", stats->ac_btime);

        printllu("  elapsed", stats->ac_etime);
        printllu("  user", stats->ac_utime);
        printllu("  system", stats->ac_stime);
        printf("memory:\n");
        printf("  bytetime:\n");
        printllu("    rss", stats->coremem);
        printllu("    vsz", stats->virtmem);
        printf("  peak:\n");
        printllu("    rss", stats->hiwater_rss);
        printllu("    vsz", stats->hiwater_vm);
        printf("io:\n");
        printf("  bytes:\n");
        printllu("    read", stats->read_char);
        printllu("    write", stats->write_char);
        printf("  syscalls:\n");
        printllu("    read", stats->read_syscalls);
        printllu("    write", stats->write_syscalls);
    }
    return 0;
}
