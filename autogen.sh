#!/bin/sh
if [ `id -u` == 0 ] ; then
	_PREFIXED=0
else
	_PREFIXED=1
fi

_STANDALONE=0
standalone() {
	_STANDALONE=1
	echo "[!] Standalone is a stub for now!"
	exit 1
}

prefixed() {
	_PREFIXED=1	
}

eval $*

# BEGIN CONFIG
if [ 'x'$PREFIX == 'x' ] ; then
	PREFIX="/usr"
fi
echo "[*] Using prefix: $PREFIX"

if [ 'x'$PYTHON == 'x' ] ; then
	PYTHON=`type -P python`
else
	PYTHON=`type -P $PYTHON`
fi

if [ 'x'$PYTHON == 'x' ] ; then 
	echo "[!] Python not found. If not in \$PATH, set PYTHON variable." >&2
	exit 1
fi
echo "[*] Python binary: $PYTHON"

if [ 'x'$VERSION == 'x' ] ; then
	VERSION=`python -c "import sys; print sys.version[:3]"`
fi

echo "[*] Python version: $VERSION"

if [ $_PREFIXED -gt 0 ] ; then
	echo "[*] Doing prefixed (rootless) installation"
else
	echo "[*] Doing normal installation (may require root)"
fi
echo "Ready to install [y/N]? \c"
read _ready

if [ ! 'x'$_ready == 'xy' ] ; then
	echo "Aborting."
	exit 1
fi

# BEGIN INSTALLATION
_install_standalone() {
	echo "Stub"
}

_install_prefixed() {
	export PYTHONPATH="${PREFIX}/lib/python${VERSION}/site-packages"
	mkdir -p $PYTHONPATH
	if [ $? -gt 0 ] ; then
		echo "[!] ${PREFIX} not writable. Aborting."
		exit 1
	fi
	$PYTHON setup.py install --prefix=${PREFIX} >/dev/null
	echo "[-] It is recommended that you add ${PREFIX}/bin to your PATH variable, and ${PYTHONPATH} to your PYTHONPATH variable."
}

_install() {
	echo "[*] Installing..."
	$PYTHON setup.py install >/dev/null
}

if [ $_PREFIXED -gt 0 ] ; then
	_install_prefixed
else
	_install
fi

echo "[*] Installation complete."
