# Post-Quantum Secure OpenID Connect using KEMTLS

## Overview
This project implements OpenID Connect with KEMTLS (Key Encapsulation Mechanism Transport Layer Security) for post-quantum secure authentication. All traditional TLS communication is replaced with KEMTLS, and all digital signatures use NIST-standardized post-quantum algorithms.

## Architecture
- **Transport Layer**: KEMTLS with Kyber KEM
- **Signature Scheme**: Dilithium (NIST standardized)
- **Protocol**: OpenID Connect 1.0 (unchanged at application layer)

## Components
1. **PQ Crypto Layer**: Wrappers for Kyber KEM and Dilithium signatures
2. **KEMTLS**: Custom implementation of KEM-based TLS handshake
3. **PQ-JWT**: JWT/JWS with post-quantum signatures
4. **OIDC Server**: Authorization and token endpoints
5. **OIDC Client**: Authentication flow and token validation
6. **Benchmarking**: Performance measurement suite

## Setup

### Prerequisites
- Python 3.8+
- liboqs (Open Quantum Safe library)

### Installation

1. Install liboqs:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind

git clone -b main https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local ..
ninja
sudo ninja install
cd ../..
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

1. Test PQ cryptography:
```bash
python3 -m src.pq_crypto.test_crypto
```

2. Run OIDC server:
```bash
python3 -m src.oidc.server
```

3. Run demo authentication flow:
```bash
python3 -m examples.demo_flow
```

4. Run benchmarks:
```bash
python3 -m src.benchmarks.run_benchmarks
```

## Project Structure
```
PQC/
├── README.md
├── requirements.txt
├── docs/                       # Technical documentation
├── src/
│   ├── pq_crypto/             # Post-quantum crypto wrappers
│   ├── kemtls/                # KEMTLS implementation
│   ├── oidc/                  # OpenID Connect server/client
│   └── benchmarks/            # Performance measurement
├── tests/                      # Unit and integration tests
├── examples/                   # Demo scripts
└── results/                    # Benchmark results
```

## Security Features
- ✅ Zero classical cryptography (no RSA, no ECC)
- ✅ NIST-standardized post-quantum algorithms
- ✅ Forward secrecy via KEMTLS
- ✅ Post-quantum authenticated key exchange
- ✅ PQ-signed ID tokens and JWTs

## Benchmarking
Performance metrics measured:
- KEMTLS handshake latency
- Token signing/verification time
- Message sizes (ciphertext, signatures)
- End-to-end authentication latency

## References
- [KEMTLS Paper](https://eprint.iacr.org/2020/534.pdf)
- [OpenID Connect Core Spec](https://openid.net/specs/openid-connect-core-1_0.html)
- [liboqs Documentation](https://github.com/open-quantum-safe/liboqs)
- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)

## License
Educational/Research Project

## Authors
PQC Project Team
