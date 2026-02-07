# QUICK START - Run Your Post-Quantum OIDC System

## 🚀 Fastest Way to See It Working

```bash
cd /home/aniket/PQC
source setup_env.sh
python3 examples/demo_full_flow.py
```

Press Enter when prompted to see all demos.

---

## 📺 What You'll See

### Demo 1: Complete OIDC Flow
```
✓ User authentication
✓ Authorization code generation
✓ Token exchange
✓ PQ-signed ID token (ML-DSA-44)
✓ Token verification (0.1ms)
✓ User profile extraction
```

### Demo 2: Security Validation
```
✓ Valid token accepted
✓ Tampered token rejected
✓ Signature verification protects data
```

### Demo 3: Algorithm Comparison
```
ML-DSA-44:   3,553 bytes (fastest)
ML-DSA-65:   4,738 bytes (balanced)
Falcon-512:  1,197 bytes (most compact) ⭐
```

---

## 🧪 Test Individual Components

```bash
# Test all crypto primitives
python3 src/pq_crypto/test_crypto.py

# Test PQ-JWT specifically
python3 src/oidc/pq_jwt.py

# Test KEMTLS protocol
python3 examples/kemtls_network_demo.py

# Quick test everything
python3 examples/interactive_demo.py
```

---

## 📊 What's Implemented

| Component | Status | File |
|-----------|--------|------|
| Kyber KEM | ✅ | `src/pq_crypto/kem.py` |
| ML-DSA Signatures | ✅ | `src/pq_crypto/signature.py` |
| KEMTLS Protocol | ✅ | `src/kemtls/` |
| PQ-JWT Handler | ✅ | `src/oidc/pq_jwt.py` |
| OIDC Server | ✅ | `src/oidc/server.py` |
| OIDC Client | ✅ | `src/oidc/client.py` |
| End-to-End Demo | ✅ | `examples/demo_full_flow.py` |

---

## 🎯 Key Features Working

- ✅ **Full OIDC authorization code flow**
- ✅ **PQ-signed ID tokens (ML-DSA-44/65/87, Falcon-512/1024)**
- ✅ **KEMTLS handshake protocol**
- ✅ **Token verification with tamper detection**
- ✅ **State/nonce security (CSRF & replay protection)**
- ✅ **Multiple algorithm support**

---

## 📈 Performance (From Real Demo)

```
ID Token Sizes:
  ML-DSA-44:  ~3.5 KB
  ML-DSA-65:  ~4.7 KB
  Falcon-512: ~1.2 KB ⭐ (smallest)

Operation Times:
  Sign:   0.12 - 0.33 ms
  Verify: 0.08 - 0.12 ms
```

---

## 🔐 Security Properties

- **Quantum-Resistant**: All algorithms are NIST PQC standards
- **Forward Secrecy**: Ephemeral KEM keys in KEMTLS
- **Tamper-Proof**: PQ signatures detect any modification
- **CSRF Protection**: State parameter validation
- **Replay Protection**: Nonce verification
- **Expiration**: Codes expire in 10 min, tokens in 1 hour

---

## 📂 Important Files

### Documentation
- `IMPLEMENTATION_COMPLETE.md` - What's done and how to demo
- `PROJECT_ROADMAP.md` - Deliverables and remaining work
- `README.md` - Project overview
- `docs/ARCHITECTURE.md` - Technical deep dive
- `docs/BEGINNER_GUIDE.md` - Novice-friendly explanation

### Demos
- `examples/demo_full_flow.py` - **START HERE** ⭐
- `examples/kemtls_network_demo.py` - KEMTLS protocol details
- `examples/interactive_demo.py` - Component-by-component demo

### Core Code
- `src/pq_crypto/` - Post-quantum primitives
- `src/kemtls/` - KEMTLS protocol
- `src/oidc/` - OIDC server, client, JWT

---

## 🎬 Demo for Video/Presentation

```bash
# 1. Start demo
python3 examples/demo_full_flow.py

# 2. Explain what's happening:
#    "User authenticates → gets authorization code → 
#     exchanges for ID token → token is PQ-signed"

# 3. Press Enter for security demo:
#    "Tampering with token → signature check fails"

# 4. Press Enter for algorithm comparison:
#    "Different algorithms, different trade-offs"

# Total runtime: ~30 seconds
# Good for: Screen recording, live demo
```

---

## ✨ One-Liner Summary

**"Complete post-quantum OpenID Connect with NIST-standardized ML-DSA signatures and KEMTLS transport - full authentication flow working end-to-end."**

---

## 🆘 If Something Doesn't Work

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check liboqs is available
python3 -c "import oqs; print('liboqs OK')"

# Verify environment
source setup_env.sh
echo $LD_LIBRARY_PATH  # Should include .local/lib

# Run quick test
python3 examples/quick_test.py
```

---

## 📞 Show Someone Right Now

```bash
cd /home/aniket/PQC && python3 examples/demo_full_flow.py
```

That's it! Press Enter twice when it pauses.

**You'll see a complete post-quantum OIDC authentication in action.** 🎉
