#!/bin/bash
# Setup script for Post-Quantum OIDC environment

export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
source venv/bin/activate

echo "✓ Post-Quantum OIDC environment activated"
echo "  - liboqs library path set"
echo "  - Python virtual environment activated"
echo ""
echo "You can now run:"
echo "  python3 src/pq_crypto/test_crypto.py    # Test PQ cryptography"
echo "  python3 src/kemtls/protocol.py          # Test KEMTLS protocol"
echo "  python3 -m examples.demo_flow            # Run full demo"
