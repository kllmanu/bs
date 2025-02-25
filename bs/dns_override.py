import socket
import dns.resolver


def resolve_with_dns(host, dns_server="8.8.8.8"):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    return resolver.resolve(host)[0].to_text()


# Override getaddrinfo before importing requests
socket.getaddrinfo, original_getaddrinfo = (
    lambda host, *args, **kwargs: original_getaddrinfo(
        resolve_with_dns(host), *args, **kwargs
    ),
    socket.getaddrinfo,
)
