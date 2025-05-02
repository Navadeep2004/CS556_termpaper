// tcp_monitor.c - Kernel module to monitor TCP metrics
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/skbuff.h>
#include <net/tcp.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("TCP Monitor");
MODULE_DESCRIPTION("TCP Performance Metrics Monitoring Module");

// Structure to store monitored metrics
struct tcp_metrics {
    u32 sending_rate;
    u32 cwnd;
    u32 rtt;
    u32 bytes_in_flight;
    u32 retransmissions;
};

// Log function for TCP metrics
static void log_tcp_metrics(struct sock *sk) {
    if (sk && sk->sk_protocol == IPPROTO_TCP) {
        struct tcp_sock *tp = tcp_sk(sk);
        
        // Calculate metrics
        u32 cwnd = tp->snd_cwnd;
        u32 rtt = tp->srtt_us >> 3; // Convert from us to ms and remove scaling
        u32 bytes_in_flight = tcp_packets_in_flight(tp) * tp->mss_cache;
        u32 retrans = tp->total_retrans;
        
        // Log metrics using printk
        printk(KERN_INFO "TCP_MONITOR: sock=%p cwnd=%u rtt=%u bytes_in_flight=%u retrans=%u\n",
               sk, cwnd, rtt, bytes_in_flight, retrans);
    }
}

// Hook function for outgoing packets
static unsigned int hook_func_out(void *priv, struct sk_buff *skb, 
                                 const struct nf_hook_state *state) {
    struct iphdr *iph;
    struct tcphdr *tcph;
    
    if (!skb)
        return NF_ACCEPT;
    
    iph = ip_hdr(skb);
    if (iph->protocol == IPPROTO_TCP) {
        tcph = tcp_hdr(skb);
        // Check if we can get to the socket
        if (skb->sk && skb->sk->sk_protocol == IPPROTO_TCP) {
            log_tcp_metrics(skb->sk);
        }
    }
    
    return NF_ACCEPT;
}

// Netfilter hook operations
static struct nf_hook_ops nfho_out = {
    .hook = hook_func_out,
    .hooknum = NF_INET_LOCAL_OUT,
    .pf = PF_INET,
    .priority = NF_IP_PRI_FIRST,
};

// Initialize module
static int __init tcp_monitor_init(void) {
    printk(KERN_INFO "TCP Monitor: Initializing module\n");
    nf_register_net_hook(&init_net, &nfho_out);
    return 0;
}

// Cleanup module
static void __exit tcp_monitor_exit(void) {
    printk(KERN_INFO "TCP Monitor: Removing module\n");
    nf_unregister_net_hook(&init_net, &nfho_out);
}

module_init(tcp_monitor_init);
module_exit(tcp_monitor_exit);
