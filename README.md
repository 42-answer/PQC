# Post-Quantum Secure OpenID Connect using KEMTLS

**Team**: ByteBreachers

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NIST PQC](https://img.shields.io/badge/NIST-Post--Quantum-green.svg)](https://csrc.nist.gov/projects/post-quantum-cryptography)
[![KEMTLS](https://img.shields.io/badge/KEMTLS-Enabled-brightgreen.svg)](https://eprint.iacr.org/2020/534.pdf)
[![OIDC 1.0](https://img.shields.io/badge/OIDC-1.0-orange.svg)](https://openid.net/specs/openid-connect-core-1_0.html)

## 🎯 Project Overview

This repository is a **research/demo prototype** that explores how post-quantum (PQ) primitives could be composed into an OIDC-style identity flow.

What it includes (repository-grounded):
1. **Post-quantum primitives via liboqs**: ML-KEM (Kyber) and PQ signature algorithms exposed through Python wrappers and benchmarks.
2. **A KEMTLS-style key-establishment workflow**: key encapsulation/decapsulation + HKDF-based key derivation (used in benchmarks and demos).
3. **An OIDC-inspired authorization-code demo flow**: issues and verifies PQ-signed ID tokens inside an in-process demo server, exposed via a Flask UI.

Important scope notes:
- This is **not a full TLS 1.3 implementation** and does **not** provide production-grade transport security.
- The OIDC pieces are **demo/simplified**; do not treat them as full OIDC Core compliance.

### 🔐 KEMTLS (Concept) vs what this repo measures

KEMTLS (as a research idea) replaces handshake signatures with KEM operations. This repository implements a **KEMTLS-style workflow** and benchmarks a **key-establishment simulation** that:
- Replaces certificate-based key exchange with Key Encapsulation Mechanisms (KEMs)
- Uses HKDF to derive session keys from the shared secret

The measured timings in `benchmark_results/` are **in-process microbenchmarks**; they should not be interpreted as full network handshake latency, and this README does not claim cross-project speedups.

---

## 🏗️ Architecture

### Four-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: OpenID Connect Protocol (Unchanged)               │
│  • Authorization Code Flow                                  │
│  • Token Endpoint                                           │
│  • UserInfo Endpoint                                        │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Application Security (JWT/JWS with PQ Signatures) │
│  • ID Token Signing (ML-DSA/Falcon)                         │
│  • Access Token Generation                                  │
│  • Token Verification                                       │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: KEMTLS Protocol (Replaces TLS)                    │
│  • KEM-based Handshake (Kyber)                              │
│  • Session Key Derivation (HKDF)                            │
│  • (Demo) Session keys derived; transport encryption is not implemented here │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Post-Quantum Cryptographic Primitives             │
│  • Kyber KEM (NIST FIPS 203 - ML-KEM)                       │
│  • ML-DSA Signatures (NIST FIPS 204 - Dilithium)            │
│  • Falcon signatures (available via liboqs; not a NIST FIPS standard) │
│  • liboqs Integration                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Components

### 1. **Post-Quantum Crypto Layer** (`src/pq_crypto/`)
Wrappers for NIST-standardized post-quantum algorithms:
- **KEM**: Kyber512/768/1024 (ML-KEM)
- **Signatures**: ML-DSA-44/65/87 (Dilithium), Falcon-512/1024
- **Utilities**: Key derivation, hashing, nonce generation

### 2. **KEMTLS Implementation** (`src/kemtls/`)
Prototype KEMTLS-style components (demo / educational):
- Protocol state machine (CLIENT_HELLO, SERVER_HELLO, etc.)
- Server and client implementations
- Certificate format with PQ keys
- Session management

### 3. **PQ-JWT Handler** (`src/oidc/pq_jwt.py`)
JWT/JWS with post-quantum signatures:
- Standard JWT format (header.payload.signature)
- PQ signature algorithms in "alg" field
- Token creation and verification
- Claims validation

### 4. **OIDC Server** (`src/oidc/server.py`)
In-memory OIDC-inspired demo server:
- Authorization endpoint
- Token endpoint
- UserInfo endpoint
- Client registration
- User management

### 5. **OIDC Client** (`src/oidc/client.py`)
Relying party demo client:
- Authorization flow initiation
- Token exchange
- Token verification
- UserInfo retrieval is not implemented in the demo client

### 6. **Benchmarking Suite** (`src/benchmarks/`)
Comprehensive performance measurement:
- Cryptographic operation benchmarks
- Protocol-level benchmarks
- Statistical analysis
- PDF report generation

---

## 🚀 Complete Setup Instructions

### Prerequisites
- **Python 3.8+** (check with `python3 --version`)
- **Linux/macOS** (tested on Ubuntu 20.04+)
- **Internet connection** (for initial setup)

---

### Step 1: Install System Dependencies & liboqs

Run these commands one by one (copy-paste):

```bash
# Update package manager
sudo apt-get update

# Install build dependencies
sudo apt-get install -y astyle cmake gcc ninja-build libssl-dev \
    python3-pytest python3-pytest-xdist unzip xsltproc doxygen \
    graphviz python3-yaml valgrind python3-pip python3-venv

# Clone liboqs library
cd ~
git clone -b main https://github.com/open-quantum-safe/liboqs.git
cd liboqs

# Build liboqs (with shared library support)
# If build directory already exists, use: cd build && rm -rf * instead
mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_SHARED_LIBS=ON ..
ninja

# Install liboqs
sudo ninja install
sudo ldconfig

# Verify installation - should show .so files
ls /usr/local/lib/liboqs*
```

**Expected result**: You should see `liboqs.so.5` file listed.

---

### Step 2: Clone and Setup This Project

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/42-answer/PQC.git
cd PQC

# Run automated setup (creates venv, installs dependencies)
source setup_env.sh
```

**What this does:**
- ✅ Creates Python virtual environment (`venv/`)
- ✅ Activates the virtual environment
- ✅ Upgrades pip to latest version
- ✅ Installs all Python dependencies from requirements.txt
- ✅ Sets environment variables for liboqs

**Expected output:**
```
Creating virtual environment...
Upgrading pip...
Installing Python dependencies...
✓ Post-Quantum OIDC environment activated
```

---

### Step 3: Verify Installation

```bash
# Test that liboqs-python is working
python -c "import oqs; print('liboqs-python:', oqs.oqs_version())"

# Expected output: liboqs-python: 0.14.0 or 0.15.0
```

If you see an error, check:
- **Codespaces**: liboqs is installed: `ls $HOME/.local/lib/liboqs*`
- **Local machine**: liboqs is installed: `ls /usr/local/lib/liboqs*`
- Library path is set: `echo $LD_LIBRARY_PATH` (should include `/usr/local/lib` or `$HOME/.local/lib`)
- Re-run setup: `source setup_env.sh`

---

### Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'oqs'`

**Solution**:
```bash
source setup_env.sh
pip install --upgrade liboqs-python
```

**Problem**: `ImportError: liboqs.so: cannot open shared object file`

**Solution**:
```bash
# Re-run setup to set library path
source setup_env.sh

# Or manually set the path:
export LD_LIBRARY_PATH=$HOME/.local/lib:/usr/local/lib:$LD_LIBRARY_PATH
```

**Problem**: `pip install` fails with dependency conflicts

**Solution**:
```bash
rm -rf venv
python3 -m venv venv
source setup_env.sh
```

---

### Quick Start (After Initial Setup)

```bash
cd PQC
source setup_env.sh
python ui/app.py
```

Then open your browser to `http://localhost:5000`

### Notes
- **No .env file required** - All configuration is built-in
- **Every session**: Run `source setup_env.sh` after opening the project
- **Deactivation**: Run `deactivate` to exit virtual environment

---

## 🎮 Running the Project - All Options

### OPTION A: Interactive Web Interface

**Launch the web-based demonstration interface:**

```bash
cd PQC
source setup_env.sh
python ui/app.py
```

Then open your browser to: **http://localhost:5000**

**Available Demonstrations:**
1. **Dashboard** - Project overview and navigation
2. **KEMTLS Handshake** - Interactive handshake demonstration with performance metrics
3. **Digital Signatures** - Testing interface for all PQ signature algorithms (ML-DSA, Falcon)
4. **JWT Operations** - Token creation and verification with post-quantum signatures
5. **Complete OIDC Flow** - End-to-end authentication flow demonstration
6. **Benchmarks** - Interactive performance data visualization
7. **Architecture** - System architecture and component overview

**Note**: All cryptographic operations are executed in real-time using liboqs implementation.

---

### OPTION B: Cryptographic Test Suite

**Execute comprehensive cryptographic validation:**

```bash
cd ~/PQC
source setup_env.sh
python src/pq_crypto/test_crypto.py
```

**Expected output:** ✓ ALL POST-QUANTUM CRYPTOGRAPHY TESTS PASSED!

**This tests:**
- ✅ Kyber KEM (3 variants: 512/768/1024)
- ✅ ML-DSA Signatures (3 variants: 44/65/87)
- ✅ Falcon Signatures (2 variants: 512/1024)
- ✅ Key generation, encryption/signing, decryption/verification
- ✅ Error handling for invalid signatures

---

### OPTION C: Performance Benchmark Generation

**Execute complete benchmark suite (32 operations):**

```bash
cd ~/PQC
source setup_env.sh
python -m src.benchmarks.run_benchmarks
```

**What this does:**
- Benchmarks 9 KEM operations (Kyber 512/768/1024)
- Benchmarks 15 signature operations (ML-DSA + Falcon, all variants)
- Benchmarks 6 JWT operations (create/verify with different algorithms)
- Benchmarks complete KEMTLS handshake
- Benchmarks end-to-end OIDC authentication flow
- Uses 100 iterations by default for microbenchmarks (see `src/benchmarks/run_benchmarks.py`)
- Saves results to `benchmark_results/` directory

**Generated files:**
- `benchmark_results/benchmark_results.json` (raw data)
- `benchmark_results/benchmark_results.csv` (spreadsheet format)

**Time:** ~30-60 seconds

---

### OPTION D: PDF Report Generation

**Generate comprehensive performance analysis report:**

```bash
cd ~/PQC
source setup_env.sh
python -m src.benchmarks.generate_pdf_report
```

**What this creates:**
- `BenchmarkResults.pdf` (10-page report)
  - Performance comparison graphs
  - Statistical tables
  - Analysis and recommendations
  - Algorithm comparison charts

**Prerequisites:** Benchmark data must exist (run Option C first if needed)

**Time:** ~5-10 seconds

---

### OPTION E: Individual Demonstration Scripts

**Execute specific demonstration modules:**

#### 1. **Complete OIDC Authentication Flow**
```bash
cd ~/PQC
source setup_env.sh
python examples/demo_full_flow.py
```
Shows complete OAuth 2.0 authorization code flow with PQ cryptography.

#### 2. **KEMTLS Network Handshake**
```bash
cd ~/PQC
source setup_env.sh
python examples/kemtls_network_demo.py
```
Demonstrates client-server KEMTLS handshake with session establishment.

#### 3. **Interactive Command-Line Demo**
```bash
cd ~/PQC
source setup_env.sh
python examples/interactive_demo.py
```
Step-by-step menu-driven demo of all features.

#### 4. **Quick Feature Test**
```bash
cd ~/PQC
source setup_env.sh
python examples/quick_test.py
```
Rapid test of all major components (< 5 seconds).

---

### OPTION F: Web API Endpoint Validation

**Validate all Flask REST API endpoints:**

```bash
cd ~/PQC
source setup_env.sh

# In terminal 1: Start UI server
python ui/app.py

# In terminal 2: Run endpoint tests
python test_ui_endpoints.py
```

**What this tests:**
- JWT creation API
- OIDC flow API
- Signature testing API
- KEMTLS handshake API
- All REST endpoints return valid JSON

---

### OPTION G: Benchmark Data Inspection

**Access pre-generated performance results:**

#### View JSON data:
```bash
cd ~/PQC
cat benchmark_results/benchmark_results.json | python -m json.tool | less
```

#### View CSV data:
```bash
cd ~/PQC
column -t -s, benchmark_results/benchmark_results.csv | less
```

#### View PDF report:
```bash
cd ~/PQC
xdg-open BenchmarkResults.pdf
# Or: evince BenchmarkResults.pdf
# Or: open BenchmarkResults.pdf  (macOS)
```

---

## OPTION H: Complete Evaluation Sequence

**Execute comprehensive demonstration workflow:**

```bash
cd ~/PQC
source setup_env.sh

# 1. Verify installation with tests
echo "=== Step 1: Running Tests ==="
python src/pq_crypto/test_crypto.py

# 2. Generate fresh benchmark data
echo -e "\n=== Step 2: Running Benchmarks ==="
python -m src.benchmarks.run_benchmarks

# 3. Generate PDF report
echo -e "\n=== Step 3: Generating PDF Report ==="
python -m src.benchmarks.generate_pdf_report

# 4. Run quick demo
echo -e "\n=== Step 4: Quick Feature Demo ==="
python examples/quick_test.py

# 5. Show benchmark summary
echo -e "\n=== Step 5: Performance Summary ==="
echo "KEMTLS Handshake: $(grep 'Full KEMTLS Handshake' benchmark_results/benchmark_results.csv | cut -d',' -f3) ms"
echo "Complete OIDC Flow: $(grep 'End-to-End OIDC Flow' benchmark_results/benchmark_results.csv | cut -d',' -f3) ms"

# 6. Start interactive UI
echo -e "\n=== Step 6: Starting Web UI ==="
echo "Open http://localhost:5000 in your browser"
python ui/app.py
```

**Total time:** ~2-3 minutes + interactive exploration

---

## 📁 Where to Find Generated Data

After running benchmarks and tests, find results here:

```bash
cd ~/PQC

# Benchmark results (raw data)
ls -lh benchmark_results/
# → benchmark_results.json (detailed timing data)
# → benchmark_results.csv (spreadsheet format)

# PDF report (visual analysis)
ls -lh BenchmarkResults.pdf
# → 10-page report with graphs and tables

# Technical documentation
ls -lh TechnicalDocumentation.md
# → 8,500-word comprehensive guide

# Project overview
ls -lh README.md
# → This file
```

---

## 🆘 Troubleshooting

### Issue: "liboqs not found"
```bash
# Solution: Set library path
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
# Or re-run: source setup_env.sh
```

### Issue: "Module not found"
```bash
# Solution: Set Python path
export PYTHONPATH=/home/aniket/PQC:$PYTHONPATH
# Or re-run: source setup_env.sh
```

### Issue: "Flask not installed"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: "Permission denied"
```bash
# Solution: Use sudo for system installs
sudo ninja install  # For liboqs
sudo ldconfig       # Update library cache
```

### Issue: Port 5000 already in use
```bash
# Solution: change the port in ui/app.py (look for app.run(..., port=5000))
```

---

## ⚡ Quick Command Reference

**One-liner to run UI:**
```bash
cd ~/PQC && source setup_env.sh && python ui/app.py
```

**One-liner to run tests:**
```bash
cd ~/PQC && source setup_env.sh && python src/pq_crypto/test_crypto.py
```

**One-liner to generate benchmarks:**
```bash
cd ~/PQC && source setup_env.sh && python -m src.benchmarks.run_benchmarks && python -m src.benchmarks.generate_pdf_report
```

**One-liner to see project structure:**
```bash
cd ~/PQC && tree -L 2 -I 'venv|__pycache__|.git'
```

---

## Evaluation Guide

### Rapid Deployment Instructions:

**1. Launch Web Interface (30 seconds):**
```bash
cd ~/PQC && source setup_env.sh && python ui/app.py
```
Access http://localhost:5000 for interactive feature demonstration.

**2. Complete Data Generation (2 minutes):**
```bash
cd ~/PQC && source setup_env.sh
python src/pq_crypto/test_crypto.py              # Run tests
python -m src.benchmarks.run_benchmarks          # Generate data
python -m src.benchmarks.generate_pdf_report     # Create PDF
```

**3. Results and Documentation:**
- **Web Interface**: http://localhost:5000 (interactive demonstrations)
- **PDF Report**: `BenchmarkResults.pdf` (graphical analysis and performance tables)
- **Raw Data**: `benchmark_results/*.json` and `*.csv` (structured performance metrics)
- **Technical Documentation**: `TechnicalDocumentation.md` (comprehensive 8,500-word guide)

### What Each Option Does:

| Option | Purpose | Time | Command |
|--------|---------|------|---------|
| **A - Web UI** | Interactive demos | 30 sec | `python ui/app.py` |
| **B - Tests** | Verify all crypto works | 10 sec | `python src/pq_crypto/test_crypto.py` |
| **C - Benchmarks** | Generate performance data | 60 sec | `python -m src.benchmarks.run_benchmarks` |
| **D - PDF Report** | Create visual report | 10 sec | `python -m src.benchmarks.generate_pdf_report` |
| **E - Demos** | Individual feature demos | 5-20 sec | `python examples/*.py` |
| **F - API Tests** | Test web endpoints | 10 sec | `python test_ui_endpoints.py` |
| **G - View Data** | See existing results | Instant | `cat benchmark_results/*.json` |
| **H - Complete** | Everything in sequence | 3 min | See Option H above |

### Deliverables Location:

```
📁 PQC/
  ├── 📄 README.md                      ← You are here
  ├── 📄 TechnicalDocumentation.md      ← Full technical guide (8,500 words)
  ├── 📊 BenchmarkResults.pdf           ← Performance report with graphs
  ├── 📂 src/                           ← Source code (4,583 lines)
  ├── 🌐 ui/                            ← Interactive web interface
  ├── 📈 benchmark_results/             ← Raw performance data (JSON/CSV)
  └── 🧪 examples/                      ← Demo scripts
```

---

## 📊 Performance Results (from stored artifacts)

All numbers should be taken from the checked-in artifacts in [benchmark_results/](benchmark_results/):
- [benchmark_results/benchmark_results.csv](benchmark_results/benchmark_results.csv)
- [benchmark_results/benchmark_results.json](benchmark_results/benchmark_results.json)

From the current checked-in CSV (in-process microbenchmarks):
- **Full KEMTLS Handshake** (simulation): ~0.0409 ms mean (50 iterations)
- **End-to-End OIDC Flow** (in-process demo sequence): ~0.2049 ms mean (20 iterations)

For plots and tables, use the LaTeX report pipeline in [report/](report/).

---

## 📁 Project Structure

```
PQC/
├── README.md                       # Project overview and documentation
├── TechnicalDocumentation.md       # Comprehensive technical guide
├── BenchmarkResults.pdf            # Performance analysis report
├── requirements.txt                # Python dependencies
├── setup_env.sh                    # Environment setup script
├── config.py                       # Configuration settings
│
├── src/                            # Source code (4,583 lines)
│   ├── pq_crypto/                  # Post-quantum crypto wrappers
│   │   ├── kem.py                  # Kyber KEM implementation
│   │   ├── signature.py            # ML-DSA/Falcon signatures
│   │   ├── utils.py                # Cryptographic utilities
│   │   └── test_crypto.py          # Crypto unit tests
│   │
│   ├── kemtls/                     # KEMTLS protocol implementation
│   │   ├── protocol.py             # Core protocol, message types
│   │   ├── server.py               # KEMTLS server
│   │   └── client.py               # KEMTLS client
│   │
│   ├── oidc/                       # OpenID Connect implementation
│   │   ├── pq_jwt.py               # PQ-JWT handler
│   │   ├── server.py               # OIDC Authorization Server
│   │   ├── client.py               # OIDC Relying Party
│   │   └── kemtls_transport.py     # KEMTLS integration
│   │
│   ├── benchmarks/                 # Performance benchmarking
│   │   ├── run_benchmarks.py       # Benchmark suite runner
│   │   └── generate_pdf_report.py  # PDF report generator
│   │
│   └── docs/                       # Documentation generation
│       └── generate_technical_doc.py  # Technical doc generator
│
├── tests/                          # Testing infrastructure
│   └── __init__.py                 # Test package initialization
│
├── examples/                       # Demo scripts
│   ├── demo_full_flow.py           # Complete OIDC flow demo
│   ├── interactive_demo.py         # Interactive demonstration
│   ├── kemtls_network_demo.py      # KEMTLS handshake demo
│   └── quick_test.py               # Quick functionality test
│
├── ui/                             # Interactive web interface
│   ├── app.py                      # Flask application
│   └── templates/                  # HTML templates (8 files)
│       ├── index.html              # Dashboard
│       ├── kemtls_demo.html        # KEMTLS demonstration
│       ├── signatures_demo.html    # Signature testing
│       ├── jwt_demo.html           # JWT creation/verification
│       ├── oidc_demo.html          # OIDC flow demonstration
│       ├── benchmarks.html         # Performance data viewer
│       ├── architecture.html       # System architecture
│       └── base.html               # Base template
│
├── benchmark_results/              # Performance data
│   ├── benchmark_results.json      # Raw benchmark data (32 operations)
│   └── benchmark_results.csv       # CSV format for analysis
│
└── docs/                           # Additional documentation
    ├── ARCHITECTURE.md             # Detailed system architecture
    └── QUICKSTART.md               # Getting started guide
```

**Total Implementation**: 4,583 lines of Python code across 19 source files

---

## 🔐 Security Features

### ✅ Post-Quantum Primitives (Scope)
- Focuses on **PQ public-key primitives** for KEM and signatures (no RSA/ECC/DH in the core demo paths).
- Uses **ML-KEM (FIPS 203)** and **ML-DSA (FIPS 204)** via liboqs.
- Includes Falcon via liboqs for experimentation; it is **not** a NIST FIPS-standard algorithm.

### ✅ Forward Secrecy
- **Ephemeral KEM keys** - New keypair for each handshake
- **Session key derivation** - HKDF with unique session context
- **No key reuse** - Past sessions remain secure if long-term keys compromised

### ✅ Authentication
- **Mutual authentication** - Server authenticated via KEMTLS certificate
- **ID token signatures** - User identity cryptographically signed
- **Token verification** - Signature validation before access grant

### ✅ Protocol Alignment (Demo)
- Uses an **authorization-code style** sequence inspired by OAuth 2.0 / OIDC.
- Uses JWT/JWS containers (RFC 7519 / 7515) with PQ signature algorithms.
- Some endpoints/steps (notably UserInfo) are simplified for demo purposes.

---

## 🧪 Testing & Verification

This repo contains lightweight demo validations rather than a full unit-test suite.

Useful checks:
```bash
source setup_env.sh

# Crypto sanity checks
python src/pq_crypto/test_crypto.py

# Start UI (terminal 1)
python ui/app.py

# Smoke-test UI JSON endpoints (terminal 2)
python test_ui_endpoints.py
```

---

## 📈 Benchmarking

### Running Benchmarks
```bash
# Execute full benchmark suite
python -m src.benchmarks.run_benchmarks

# Results saved to:
#  - benchmark_results/benchmark_results.json
#  - benchmark_results/benchmark_results.csv

# Generate PDF report
python -m src.benchmarks.generate_pdf_report
# Output: BenchmarkResults.pdf
```

### Benchmark Metrics Measured
1. **Cryptographic-Level**:
   - KEM: keygen, encapsulation, decapsulation (9 benchmarks)
   - Signatures: keygen, sign, verify (15 benchmarks)
   - Individual operation timings and sizes

2. **Protocol-Level**:
   - Complete KEMTLS handshake (1 benchmark)
   - JWT creation and verification (6 benchmarks)
   - End-to-end OIDC authentication flow (1 benchmark)
   - Total latencies and message sizes

**Total**: 32 operations benchmarked with statistical analysis (mean, median, stdev, min, max)

---

## 🎓 Algorithm Selection Guide

### Key Encapsulation (KEM)

| Algorithm | Security Level | Public Key | Ciphertext | Use Case |
|-----------|----------------|------------|------------|----------|
| **Kyber512** | NIST Level 1 | 800 bytes | 768 bytes | High performance |
| **Kyber768** ⭐ | NIST Level 3 | 1,184 bytes | 1,088 bytes | **Recommended** |
| **Kyber1024** | NIST Level 5 | 1,568 bytes | 1,568 bytes | Maximum security |

**Recommendation**: **Kyber768** - Best balance of security and performance

### Digital Signatures

| Algorithm | Security Level | Public Key | Signature | Keygen | Sign | Verify |
|-----------|----------------|------------|-----------|--------|------|--------|
| **ML-DSA-44** ⭐ | NIST Level 2 | 1,312 bytes | 2,420 bytes | 0.0325ms | 0.0711ms | 0.0262ms |
| **ML-DSA-65** | NIST Level 3 | 1,952 bytes | 3,309 bytes | 0.0500ms | 0.2138ms | 0.0431ms |
| **ML-DSA-87** | NIST Level 5 | 2,592 bytes | 4,627 bytes | 0.0683ms | 0.2884ms | 0.0893ms |
| **Falcon-512** 🪶 | NIST Level 1 | 897 bytes | **656 bytes** | 5.3442ms | 0.2212ms | 0.0440ms |
| **Falcon-1024** | NIST Level 5 | 1,793 bytes | 1,269 bytes | 15.8008ms | 0.3607ms | 0.0655ms |

Note: Falcon is included for comparison via liboqs and stored benchmark artifacts; it is not a NIST FIPS standard.

**Recommendations**:
- **General use**: **ML-DSA-44** - Fast, NIST Level 2 security
- **Bandwidth-constrained**: **Falcon-512** - Smallest signatures (656 bytes)
- **High security**: ML-DSA-65 or ML-DSA-87

---

## 📚 Technical Documentation

### Core Documentation
- **[README.md](README.md)** - This file, project overview and quick start
- **[TechnicalDocumentation.md](TechnicalDocumentation.md)** - Comprehensive technical guide (8,500 words)
- **[BenchmarkResults.pdf](BenchmarkResults.pdf)** - Performance analysis with graphs
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system architecture
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Step-by-step tutorial

### Performance Data
- **[benchmark_results/](benchmark_results/)** - Raw benchmark data (JSON/CSV)
- **32 operations benchmarked** - KEM, signatures, JWT, KEMTLS, OIDC
- **Statistical analysis** - Mean, median, stdev, min, max

---

## 🔬 Research Background

### KEMTLS
This project is inspired by KEMTLS and includes KEMTLS-style demo components; see the paper for the full protocol design:

> Schwabe, P., Stebila, D., & Wiggers, T. (2020).  
> **More Efficient Post-Quantum KEMTLS with Pre-Distributed Public Keys**  
> IACR Cryptology ePrint Archive, Report 2020/534  
> https://eprint.iacr.org/2020/534.pdf

**Key differences from TLS**:
- Replaces Diffie-Hellman with KEM operations
- Uses KEM keys in certificates instead of signature keys
- Derives session keys from a shared secret (this repo uses HKDF in the demo/benchmarks)

### Post-Quantum OIDC
Implementation builds upon methodology from:

> Schardong, F., Custódio, R., & Perin, L. P. (2023).  
> **Post-Quantum OpenID Connect**.

This repository is conceptually related (OIDC + PQ primitives), but it does not claim a like-for-like performance comparison against other implementations.

### NIST Post-Quantum Standardization
NIST FIPS standards (as of the standardization set used by this repo):
- **ML-KEM** (Kyber) - FIPS 203
- **ML-DSA** (Dilithium) - FIPS 204
- **SLH-DSA** (SPHINCS+) - FIPS 205

Falcon is referenced as an available algorithm in liboqs and in the benchmark artifacts, but it is not a NIST FIPS standard.

---

## 📖 References

### Standards & Specifications
1. **[OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)** - OIDC specification
2. **[OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)** - Authorization framework
3. **[JWT RFC 7519](https://tools.ietf.org/html/rfc7519)** - JSON Web Tokens
4. **[JWS RFC 7515](https://tools.ietf.org/html/rfc7515)** - JSON Web Signatures

### Post-Quantum Cryptography
5. **[NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)** - Standardization effort
6. **[NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final)** - ML-KEM (Kyber)
7. **[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final)** - ML-DSA (Dilithium)
8. **[NIST FIPS 205](https://csrc.nist.gov/pubs/fips/205/final)** - SLH-DSA (SPHINCS+)

### Implementation Libraries
9. **[liboqs](https://github.com/open-quantum-safe/liboqs)** - Open Quantum Safe cryptographic library
10. **[KEMTLS Paper](https://eprint.iacr.org/2020/534.pdf)** - KEMTLS protocol specification

---

## 🤝 Contributing

This is an educational/research project. Contributions welcome:
- Algorithm optimizations
- Additional benchmarks
- Documentation improvements
- Bug reports

---

## ⚖️ License

**Educational/Research Project**

Developed for academic purposes. Not intended for production use without security audit.

Uses:
- **liboqs** - MIT License
- **NIST PQC algorithms** - Public domain

---

## 👥 Authors

**Team ByteBreachers**  
Post-Quantum Cryptography Research Project  
February 2026

---

## 🎯 Project Status

**Status**: ✅ demo prototype (UI + benchmarks + report pipeline)

This repository is suitable for demonstrations and benchmarking, but it is not production-hardened and does not claim full standards compliance.

---

## 🚀 Next Steps

### For Development
```bash
# Explore the code
cd src/
ls -R

# Read technical documentation
cat TechnicalDocumentation.md

# Try interactive demos
python ui/app.py
```

### For Submission
```bash
# All deliverables ready:
# ✓ README.md (this file)
# ✓ TechnicalDocumentation.md (8,500 words)
# ✓ BenchmarkResults.pdf (graphs and analysis)
# ✓ Source code (src/ directory)
# ✓ Interactive UI (ui/ directory)
```

### For Further Research
- Optimize handshake protocol (reduce round-trips)
- Implement client authentication with KEMTLS
- Add support for additional PQ algorithms (e.g., SPHINCS+)
- Integrate with real-world OIDC providers
- Conduct formal security analysis

---

**Questions?** See [TechnicalDocumentation.md](TechnicalDocumentation.md) for detailed explanations or [docs/QUICKSTART.md](docs/QUICKSTART.md) for tutorials.

**Issues?** Run tests: `python src/pq_crypto/test_crypto.py` or check UI: `python ui/app.py`
