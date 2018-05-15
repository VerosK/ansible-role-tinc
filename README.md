
# VerosK.tinc

This is backup of my try to evaluate tinc as full-mesh VPN.

## How to use:

Setup some nodes, add `tinc_ip` host variable to private address. Apply the role

    # hosts
    [all]
    apple      tinc_ip=192.168.101.1
    bubble     tinc_ip=192.168.102.1
    kitty      tinc_ip=192.168.103.1

Keypairs are going to be generated on managed machines and downloaded to fact `tinc_node_public_key`



## License

BSD

## Author Information

[Veros Kaplan](https://github.com/verosk/). Sponsored by [Team Solutions](https://teamguru.com/)

Inspired by [Ajgarlag.tinc](https://github.com/ajgarlag/ansible-tinc)
