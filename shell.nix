{ pkgs ? (import <nixpkgs> {}).pkgs }:
with pkgs;
mkShell {
  shellHook = ''
    # fixes libstdc++ issues and libgl.so issues
    LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/

    # Python virtual environment setup
    VENV_DIR=".venv"
    if [ ! -d "$VENV_DIR" ]; then
      echo "Creating virtual environment..."
      python -m venv $VENV_DIR
      source $VENV_DIR/bin/activate
      echo "Installing depencies..."
      pip3 install -r requirements.txt
    else
      source $VENV_DIR/bin/activate
    fi
    echo "Virtual environment activated."
  '';
}