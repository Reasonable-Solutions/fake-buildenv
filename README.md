# fake-buildenv

A small Nix flake for demonstrating user-supplied environments with the
transient execution service. The default package contains:

- Bash and GNU coreutils;
- cowsay;
- Python 3 with JupyterLab, NumPy, pandas, SciPy, scikit-learn, Matplotlib,
  and seaborn;
- Git, jq, and ripgrep;
- the Palmer Penguins CSV dataset; and
- `penguin-stats` and `penguin-demo` commands.

## Try it locally

```console
nix run
nix shell
penguin-demo
python3 --version
python3 -c 'import numpy, pandas, scipy, sklearn, matplotlib, seaborn'
jupyter lab --version
cowsay hello
```

## Try it through execd

The selected execd profile must set `allowUserEnvironments = true`.

```console
env \
  SOKK_PROFILE=gpu-shell \
  SOKK_FLAKE=github:Reasonable-Solutions/fake-buildenv \
  SOKK_SESSION=new \
ssh -tt -F /dev/null -p 2222 \
  -i "$HOME/.ssh/execd-p-carl" \
  -o CertificateFile="$HOME/.ssh/execd-p-carl-cert.pub" \
  -o IdentitiesOnly=yes \
  -o 'SendEnv=SOKK_PROFILE SOKK_FLAKE SOKK_SESSION' \
  p-carl@127.0.0.1
```

Once connected:

```console
penguin-demo
penguin-stats
jupyter lab --no-browser
```

The scientific Python stack is intentionally a reasonably large closure. A
cold machine should spend long enough evaluating and downloading it to make
execd's setup progress visible; later sessions reuse the realised Nix store
paths and should come up much faster.

`gpu-shell` still controls CPU, memory, fake-GPU, network, and lifetime policy;
this flake only supplies the filesystem environment.

## Dataset

The CSV is pinned to revision
`8957207b78d6ccd1b4654a9dd9c9041b657478ab` of
[allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins).
The Palmer Penguins data is made available under
[CC0](https://creativecommons.org/publicdomain/zero/1.0/). Please see the
upstream project for provenance and citation information.

## License

The demo code is MIT licensed. The Palmer Penguins dataset is CC0 and remains
subject to its upstream attribution and citation guidance.
