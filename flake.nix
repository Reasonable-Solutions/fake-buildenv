{
  description = "A tiny transient-execution demo environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };

          penguinsCsv = pkgs.fetchurl {
            url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv";
            hash = "sha256-8gTbLHU7CTfKrDyzUlhWLBTwc+S7x2viS0xRziJ2epM=";
          };

          penguinsData = pkgs.runCommand "palmer-penguins-data" { } ''
            install -Dm444 ${penguinsCsv} \
              "$out/share/fake-buildenv/penguins.csv"
          '';

          # Deliberately substantial: the demo is also useful for observing a
          # cold user-environment evaluation/download before subsequent runs
          # hit the Nix store cache.
          python = pkgs.python3.withPackages (packages: with packages; [
            jupyterlab
            matplotlib
            numpy
            pandas
            scikit-learn
            scipy
            seaborn
          ]);

          penguinStats = pkgs.writeShellApplication {
            name = "penguin-stats";
            runtimeInputs = [ python ];
            text = ''
              exec python3 ${./penguin_demo.py} \
                ${penguinsData}/share/fake-buildenv/penguins.csv "$@"
            '';
          };

          penguinDemo = pkgs.writeShellApplication {
            name = "penguin-demo";
            runtimeInputs = [ pkgs.cowsay penguinStats ];
            text = ''
              penguin-stats | cowsay
            '';
          };

          environment = pkgs.buildEnv {
            name = "fake-buildenv";
            paths = [
              pkgs.bashInteractive
              pkgs.coreutils
              pkgs.cowsay
              pkgs.gitMinimal
              pkgs.jq
              pkgs.ripgrep
              python
              penguinsData
              penguinStats
              penguinDemo
            ];
          };
        in
        {
          default = environment;
          inherit environment penguinDemo penguinStats penguinsData;
        });

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.penguinDemo}/bin/penguin-demo";
        };
      });
    };
}
