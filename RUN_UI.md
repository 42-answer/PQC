# Running the Post-Quantum OIDC Web UI

## Quick Start

### 1. Install Flask (if not already installed)
```bash
pip install Flask
```

### 2. Start the UI Server
```bash
cd /home/aniket/PQC
python ui/app.py
```

### 3. Open Browser
Navigate to: **http://localhost:5000**

---

## What You Can Do

The UI provides interactive demonstrations of:

### 🔑 KEMTLS Handshake
- Test Kyber512/768/1024 algorithms
- See real-time performance metrics
- View message sizes and timing breakdown

### ✍️ Digital Signatures
- Sign messages with ML-DSA or Falcon
- Verify signatures instantly
- Compare different algorithms

### 🎫 JWT Tokens
- Create post-quantum signed JWTs
- Decode and verify tokens
- See token sizes for different algorithms

### 🔐 Complete OIDC Flow
- Run full authentication flow
- Step-by-step visualization
- Performance metrics for each step

### 📊 Benchmarks
- View all 32 benchmark results
- Filter by operation type
- Compare algorithm performance

### 🏗️ Architecture
- System architecture overview
- Layer-by-layer explanation
- Component descriptions

---

## Demo Credentials

**Username:** demo_user  
**Password:** demo123

---

## Features

✅ **No Code Breakage** - UI runs independently, doesn't modify existing code  
✅ **Real-Time Demos** - All operations execute live using actual implementation  
✅ **Visual Feedback** - Color-coded results, timing metrics, size measurements  
✅ **Interactive** - Test different algorithms and parameters  
✅ **Professional** - Clean, modern interface suitable for presentations  

---

## Screenshots Available At

- Dashboard: http://localhost:5000/
- KEMTLS Demo: http://localhost:5000/demo/kemtls
- Signatures: http://localhost:5000/demo/signatures
- JWT: http://localhost:5000/demo/jwt
- OIDC Flow: http://localhost:5000/demo/oidc
- Benchmarks: http://localhost:5000/benchmarks
- Architecture: http://localhost:5000/architecture

---

## For Video Recording

1. Start UI: `python ui/app.py`
2. Open browser to http://localhost:5000
3. Screen record while demonstrating:
   - Run KEMTLS handshake
   - Test signature creation/verification
   - Create JWT token
   - Execute complete OIDC flow
   - Show benchmark results
   - Display architecture diagram

Total demo time: ~5-10 minutes

---

## Troubleshooting

**Port 5000 already in use?**
```bash
# Edit ui/app.py, change last line to:
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Flask not found?**
```bash
pip install Flask
# Or with virtual environment:
source venv/bin/activate
pip install Flask
```

**Import errors?**
Make sure you're running from the project root directory:
```bash
cd /home/aniket/PQC
python ui/app.py
```
