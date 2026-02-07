# How to Run and Test - Command Reference

## Setup (Do This Once)

```bash
cd /home/aniket/PQC
source setup_env.sh
```

## Run Options

### 🎬 Option 1: Interactive Demo (BEST for understanding)

```bash
python3 examples/interactive_demo.py
```

**What you'll see:**
- Live demonstration of quantum-safe crypto
- Simulated KEMTLS handshake with explanations
- JWT creation and verification
- How everything fits together

**Time**: 2-3 minutes (with pauses to read)

---

### ⚡ Option 2: Quick Test (Fast verification)

```bash
python3 examples/quick_test.py
```

**What you'll see:**
- All component tests run in sequence
- Pass/fail for each module
- Quick verification everything works

**Time**: 30 seconds

---

### 🔬 Option 3: Individual Tests

#### Test Cryptography
```bash
python3 src/pq_crypto/test_crypto.py
```
Output: Tests Kyber, ML-DSA, Falcon signatures

#### Test KEMTLS
```bash
python3 src/kemtls/protocol.py
python3 src/kemtls/server.py
python3 src/kemtls/client.py
```
Output: Tests handshake protocol components

#### Test JWT
```bash
python3 src/oidc/pq_jwt.py
```
Output: Tests token creation with different algorithms

---

## What Each Command Does

| Command | What It Tests | Output |
|---------|---------------|--------|
| `interactive_demo.py` | Everything with explanations | Shows how components work together |
| `quick_test.py` | All modules quickly | Pass/fail for each test |
| `pq_crypto/test_crypto.py` | Kyber + ML-DSA | Crypto operations work |
| `kemtls/*.py` | KEMTLS protocol | Handshake components work |
| `oidc/pq_jwt.py` | JWT handler | Token creation/verification |

---

## Example Output

### From interactive_demo.py:

```
🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒
POST-QUANTUM SECURE OPENID CONNECT
🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒

DEMO 1: Post-Quantum Cryptography
==================================

[Step 1] Kyber KEM - Key Exchange
👤 Alice generates Kyber keypair...
   ✓ Public key generated: 800 bytes
👤 Bob encapsulates a shared secret...
   ✓ Ciphertext: 768 bytes
👤 Alice decapsulates...
   ✅ SUCCESS! Both have same secret!

[Step 2] ML-DSA Signatures
📝 Message to sign: Hello, Post-Quantum World!
   ✓ Signature created: 2420 bytes
🔍 Verifying signature...
   ✅ Signature is VALID!

...
```

### From quick_test.py:

```
1. Testing Post-Quantum Cryptography...
   ✓ Kyber512: PASSED
   ✓ ML-DSA-44: PASSED
   ✓ Falcon-512: PASSED

2. Testing KEMTLS Protocol...
   ✓ Messages: PASSED
   ✓ Certificates: PASSED

3. Testing JWT...
   ✓ Creation: PASSED
   ✓ Verification: PASSED

✅ ALL TESTS PASSED!
```

---

## Troubleshooting

### Problem: "No module named 'oqs'"

**Solution:**
```bash
source setup_env.sh
```

### Problem: "liboqs.so not found"

**Solution:**
```bash
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```

### Problem: "Import error"

**Solution:** Make sure you're in the right directory
```bash
cd /home/aniket/PQC
source setup_env.sh
```

---

## Quick Reference

**To see what's implemented:**
```bash
python3 examples/interactive_demo.py
```

**To verify everything works:**
```bash
python3 examples/quick_test.py
```

**To test one component:**
```bash
python3 src/pq_crypto/test_crypto.py
```

---

## Summary

✅ **You have working code!**
✅ **You can test it right now!**
✅ **Demos show exactly what it does!**

**Just run:**
```bash
cd /home/aniket/PQC
source setup_env.sh
python3 examples/interactive_demo.py
```

**And watch the magic happen! 🎉**
