This is a tool that streamlines the process of updating `swift` for nixpkgs. It aims to be dirty, but quick.

Given a Swift release's full version, we want to figure out its dependency repositories by looking at its `update-checkout-config.json`. Then, we use `nix-prefetch-url --unpack *` to figure out the sha value Nix expects. Given the shas and versions, we fill it in to a template.

Obviously, this is very simplistic. Swift's full build setup could change in ways that require more project
checkouts, more source patches, etc. This tool does not help with that in any way.

Basic usage:

```
# generate the nix expression in tmp/default.nix
python3 generate.py 5.5.2 default.nix
```
