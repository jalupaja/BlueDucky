{ pkgs ? import <nixpkgs> {} }:

# Define the environment
pkgs.mkShell {
	buildInputs = with pkgs; [
		# libbluetooth-dev
		git
		gcc
		bluez
		bluez-tools
		python312
		python312Packages.pip
		python312Packages.pydbus
		python312Packages.dbus-python
		python312Packages.setuptools
		python312Packages.pybluez
	];
}
