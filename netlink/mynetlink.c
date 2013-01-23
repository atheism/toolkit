#include <linux/errno.h>
#include <linux/module.h>
#include <linux/netlink.h>
#include <linux/sched.h>
#include <net/sock.h>
#include <linux/proc_fs.h>
#include <linux/mutex.h>

#define BUF_SIZE 16384

/* just use a fake protcol number */
#define NETLINK_TEST 23

static DEFINE_MUTEX(my_nl_mutex);
static struct sock *netlink_sock;

/* process the actual message from skb */
static int my_netlink_rcv_msg(struct sk_buff *skb, struct nlmsghdr *nlh)
{
    int dst_pid;
    struct sk_buff *__skb;
    int len;

    __skb = skb_clone(skb, GFP_KERNEL);

    nlh = nlmsg_hdr(skb);
    len = skb->len;
    dst_pid = nlh->nlmsg_pid;

    printk("netlink recv: %s\n", (char *)NLMSG_DATA(nlh));

    NETLINK_CB(__skb).pid = 0;
    NETLINK_CB(__skb).dst_group = 0;
 
    return netlink_unicast(netlink_sock, __skb, dst_pid, MSG_DONTWAIT);
}

static void my_netlink_rcv(struct sk_buff *skb)
{
    mutex_lock(&my_nl_mutex);
    netlink_rcv_skb(skb, my_netlink_rcv_msg);
    mutex_unlock(&my_nl_mutex);
}

static int __init netlink_init(void)
{
    printk("insmod netlink module.\n");                                                                                                                 

    struct netlink_kernel_cfg cfg;
    cfg.groups = 0;
    //cfg.flags = 0; /* not implentmented on this kernel. */
    cfg.input = my_netlink_rcv;
    cfg.cb_mutex = &my_nl_mutex;
    cfg.bind = NULL;

    netlink_sock = netlink_kernel_create(&init_net, NETLINK_TEST, THIS_MODULE, &cfg);
    if ( !netlink_sock ) 
    {
        printk("Fail to create netlink socket.\n");
        return -ENOMEM;
    }

    return 0;
}
 
static void __exit netlink_exit(void)
{
        printk("rmmod netlink module.\n");
        sock_release(netlink_sock->sk_socket);
}

module_init(netlink_init);
module_exit(netlink_exit);
MODULE_LICENSE("GPL");


