#!/usr/bin/env python3
"""
Generate Technical Documentation PDF using ReportLab

Creates comprehensive technical documentation directly in PDF format.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from datetime import datetime
import os

def create_technical_documentation(output_file="TechnicalDocumentation.pdf"):
    """Generate technical documentation PDF."""
    
    print(f"Generating technical documentation: {output_file}")
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=inch*0.75,
        leftMargin=inch*0.75,
        topMargin=inch,
        bottomMargin=inch
    )
    
    # Container for PDF elements
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        leftIndent=20,
        fontName='Courier',
        backColor=colors.HexColor('#f4f4f4')
    )
    
    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Post-Quantum OIDC with KEMTLS", title_style))
    story.append(Paragraph("Technical Documentation", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("NIST Post-Quantum Cryptography Standards", styles['Normal']))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading1_style))
    story.append(Paragraph("""
    This document provides comprehensive technical documentation for the Post-Quantum OIDC with KEMTLS 
    implementation. The project implements OpenID Connect (OIDC) authentication using NIST-standardized 
    post-quantum cryptographic algorithms.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Features
    story.append(Paragraph("Key Features:", heading2_style))
    features = [
        "Post-Quantum Key Encapsulation: Kyber (ML-KEM) for secure key exchange",
        "Post-Quantum Digital Signatures: ML-DSA (Dilithium) and Falcon for authentication",
        "KEMTLS Protocol: TLS variant using KEMs for authentication",
        "OIDC Integration: Complete OAuth 2.0/OIDC server and client implementation",
        "Production-Ready: Comprehensive testing, benchmarking, and documentation"
    ]
    for feature in features:
        story.append(Paragraph(f"• {feature}", styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Performance Highlights
    story.append(Paragraph("Performance Highlights (see BenchmarkResults.pdf for details):", heading2_style))
    perf_data = [
        ["Operation", "Time"],
        ["KEM Operations", "0.023-0.033 ms"],
        ["Signature Operations", "0.027-0.181 ms"],
        ["KEMTLS Handshake", "0.041 ms"],
        ["End-to-End OIDC Flow", "0.240 ms"]
    ]
    perf_table = Table(perf_data, colWidths=[3*inch, 1.5*inch])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(perf_table)
    story.append(PageBreak())
    
    # System Architecture
    story.append(Paragraph("System Architecture", heading1_style))
    story.append(Paragraph("""
    The system is architected in modular layers, each handling specific concerns. The architecture
    follows a clean separation of concerns with well-defined interfaces between layers.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Architecture Layers
    story.append(Paragraph("Architecture Layers:", heading2_style))
    layers = [
        ("OIDC Layer", "Application-level authentication and authorization"),
        ("JWT Layer", "Token creation and verification with PQ signatures"),
        ("KEMTLS Layer", "Secure transport with PQ key encapsulation"),
        ("PQ Crypto Layer", "Core cryptographic primitives (KEM, signatures)"),
        ("liboqs", "Native library with NIST PQ algorithm implementations")
    ]
    for layer, desc in layers:
        story.append(Paragraph(f"<b>{layer}</b>: {desc}", styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Component Descriptions
    story.append(Paragraph("Core Components", heading1_style))
    
    # PQ Crypto Layer
    story.append(Paragraph("1. Post-Quantum Cryptography Layer (src/pq_crypto/)", heading2_style))
    story.append(Paragraph("""
    Provides high-level Python interfaces to post-quantum cryptographic primitives. Includes KEM 
    implementation using Kyber (ML-KEM), digital signatures using ML-DSA (Dilithium) and Falcon, 
    and cryptographic utilities for key derivation and management.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    crypto_modules = [
        ["Module", "Purpose", "Algorithms"],
        ["kem.py", "Key Encapsulation", "Kyber512, Kyber768, Kyber1024"],
        ["signature.py", "Digital Signatures", "ML-DSA-44/65/87, Falcon-512/1024"],
        ["utils.py", "Crypto Utilities", "HKDF key derivation"]
    ]
    crypto_table = Table(crypto_modules, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    crypto_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(crypto_table)
    story.append(Spacer(1, 0.3*inch))
    
    # KEMTLS Layer
    story.append(Paragraph("2. KEMTLS Layer (src/kemtls/)", heading2_style))
    story.append(Paragraph("""
    Implements the KEMTLS protocol for authenticated key exchange using Key Encapsulation Mechanisms 
    instead of traditional signature-based authentication. Provides certificate-based authentication 
    using PQ keys with perfect forward secrecy via ephemeral KEMs.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # JWT Layer
    story.append(Paragraph("3. JWT Layer (src/oidc/pq_jwt.py)", heading2_style))
    story.append(Paragraph("""
    Creates and verifies JSON Web Tokens with post-quantum signatures. Implements native PQ signature 
    integration in JWT format with algorithm negotiation between client and server. Tokens are 
    backward-compatible in structure and size-optimized for network transmission.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    token_sizes = [
        ["Algorithm", "Token Size", "Notes"],
        ["ML-DSA-44", "~3.5 KB", "Fast, reasonable size"],
        ["ML-DSA-65", "~4.7 KB", "Higher security"],
        ["Falcon-512", "~1.2 KB", "Smallest (66% reduction!)"]
    ]
    token_table = Table(token_sizes, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
    token_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(token_table)
    story.append(Spacer(1, 0.3*inch))
    
    # OIDC Layer
    story.append(Paragraph("4. OIDC Layer (src/oidc/)", heading2_style))
    story.append(Paragraph("""
    Full OAuth 2.0 / OpenID Connect implementation with authorization code flow. Implements standard 
    OIDC endpoints (authorize, token, userinfo) with PQ-signed ID tokens. Supports client registration, 
    token validation, and user information retrieval.
    """, styles['BodyText']))
    story.append(PageBreak())
    
    # Security Analysis
    story.append(Paragraph("Security Analysis", heading1_style))
    story.append(Paragraph("Cryptographic Strength", heading2_style))
    story.append(Paragraph("""
    All algorithms used are NIST-approved post-quantum standards providing quantum resistance 
    equivalent to or exceeding AES-128 security level.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    algo_security = [
        ["Algorithm", "Security Level", "Key Size", "Signature/CT Size"],
        ["Kyber512", "NIST Level 1", "800 B", "768 B"],
        ["Kyber768", "NIST Level 3", "1184 B", "1088 B"],
        ["ML-DSA-44", "NIST Level 2", "1312 B", "~2420 B"],
        ["ML-DSA-65", "NIST Level 3", "1952 B", "~3309 B"],
        ["Falcon-512", "NIST Level 1", "897 B", "~650 B"]
    ]
    algo_table = Table(algo_security, colWidths=[1.3*inch, 1.3*inch, 1*inch, 1.4*inch])
    algo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(algo_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Threat Model", heading2_style))
    story.append(Paragraph("<b>Protected Against:</b>", styles['BodyText']))
    threats_protected = [
        "✓ Quantum computer attacks (Shor's algorithm ineffective)",
        "✓ Man-in-the-middle attacks (KEMTLS authentication)",
        "✓ Replay attacks (nonces, timestamps in tokens)",
        "✓ Token forgery (PQ signatures)",
        "✓ Eavesdropping (encrypted channels)"
    ]
    for threat in threats_protected:
        story.append(Paragraph(threat, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Out of Scope:</b>", styles['BodyText']))
    out_of_scope = [
        "• Side-channel attacks (implementation-dependent)",
        "• Physical security",
        "• Social engineering",
        "• Endpoint compromise"
    ]
    for item in out_of_scope:
        story.append(Paragraph(item, styles['BodyText']))
    story.append(PageBreak())
    
    # Implementation Details
    story.append(Paragraph("Implementation Details", heading1_style))
    story.append(Paragraph("File Structure", heading2_style))
    
    structure = Preformatted("""
PQC/
├── src/
│   ├── pq_crypto/          # PQ cryptography primitives
│   │   ├── kem.py          # Kyber KEM implementation
│   │   ├── signature.py    # ML-DSA & Falcon signatures
│   │   └── utils.py        # Crypto utilities
│   │
│   ├── kemtls/             # KEMTLS protocol
│   │   ├── protocol.py     # Core protocol logic
│   │   ├── server.py       # Server-side KEMTLS
│   │   ├── client.py       # Client-side KEMTLS
│   │   └── certificates.py # PQ certificates
│   │
│   ├── oidc/               # OpenID Connect
│   │   ├── server.py       # OIDC Provider (IdP)
│   │   ├── client.py       # OIDC Relying Party
│   │   └── pq_jwt.py       # PQ-signed JWT tokens
│   │
│   └── benchmarks/         # Performance benchmarking
│       ├── run_benchmarks.py
│       └── generate_pdf_report.py
│
├── tests/                  # Comprehensive test suite
├── benchmark_results/      # Benchmark data and reports
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
    """, code_style)
    story.append(structure)
    story.append(Spacer(1, 0.3*inch))
    
    # API Reference
    story.append(Paragraph("API Reference", heading2_style))
    story.append(Paragraph("<b>KEM Module (pq_crypto/kem.py)</b>", styles['BodyText']))
    story.append(Paragraph("""
    KyberKEM class provides key encapsulation mechanisms. Main methods: generate_keypair() returns 
    (public_key, secret_key), encapsulate(public_key) returns (ciphertext, shared_secret), and 
    decapsulate(ciphertext, secret_key) returns shared_secret.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Signature Module (pq_crypto/signature.py)</b>", styles['BodyText']))
    story.append(Paragraph("""
    DilithiumSigner and FalconSigner classes provide digital signatures. Main methods: generate_keypair() 
    returns (public_key, secret_key), sign(message, secret_key) returns signature, and verify(message, 
    signature, public_key) returns boolean.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>JWT Module (oidc/pq_jwt.py)</b>", styles['BodyText']))
    story.append(Paragraph("""
    create_id_token(claims, algorithm, secret_key) creates signed ID token. verify_id_token(token, 
    public_key, algorithm) verifies and decodes ID token, raising ValueError if signature invalid 
    or token expired.
    """, styles['BodyText']))
    story.append(PageBreak())
    
    # Testing
    story.append(Paragraph("Testing & Quality Assurance", heading1_style))
    story.append(Paragraph("""
    The project includes comprehensive tests covering all components with unit tests for individual 
    functions/classes, integration tests for component interaction, and end-to-end tests for full 
    protocol flows.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Test Coverage:", heading2_style))
    test_coverage = [
        "✓ KEM operations (key generation, encapsulation, decapsulation)",
        "✓ Signature operations (all algorithms)",
        "✓ KEMTLS handshake (complete protocol flow)",
        "✓ JWT creation and verification",
        "✓ OIDC authorization code flow",
        "✓ Error handling and edge cases"
    ]
    for item in test_coverage:
        story.append(Paragraph(item, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Performance Analysis
    story.append(Paragraph("Performance Analysis", heading1_style))
    story.append(Paragraph("""
    Comprehensive benchmarking shows all operations complete in sub-millisecond time (except Falcon 
    key generation which takes 5-16ms). See BenchmarkResults.pdf for detailed performance graphs, 
    tables, and analysis.
    """, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    
    recommendations = [
        ["Use Case", "Recommended Algorithm", "Reason"],
        ["General Use", "ML-DSA-44", "Fast (~0.076ms), reasonable size"],
        ["Bandwidth-Limited", "Falcon-512", "Smallest tokens (~1.2KB)"],
        ["Maximum Security", "ML-DSA-87", "Highest security level"],
        ["IoT/Embedded", "Kyber512", "Fastest KEM operations"]
    ]
    rec_table = Table(recommendations, colWidths=[1.8*inch, 1.8*inch, 2.4*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(rec_table)
    story.append(PageBreak())
    
    # Deployment
    story.append(Paragraph("Deployment Guide", heading1_style))
    story.append(Paragraph("Installation Steps:", heading2_style))
    
    install_cmds = Preformatted("""
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake git python3-pip

# Install liboqs
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs && mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local ..
ninja && sudo ninja install

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
    """, code_style)
    story.append(install_cmds)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Production Considerations:", heading2_style))
    prod_considerations = [
        "<b>Security:</b> Use TLS 1.3, HSM for key storage, regular key rotation",
        "<b>Performance:</b> Cache public keys, use connection pooling, async I/O",
        "<b>Scalability:</b> Stateless design, horizontal scaling, distributed cache",
        "<b>Monitoring:</b> Log all auth attempts, set up alerting, rate limiting"
    ]
    for item in prod_considerations:
        story.append(Paragraph(f"• {item}", styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # References
    story.append(Paragraph("References", heading1_style))
    story.append(Paragraph("<b>NIST Standards:</b>", styles['BodyText']))
    nist_refs = [
        "• FIPS 203: Module-Lattice-Based KEM (ML-KEM / Kyber)",
        "• FIPS 204: Module-Lattice-Based Digital Signature (ML-DSA / Dilithium)",
        "• FIPS 205: Stateless Hash-Based Digital Signature (SLH-DSA / SPHINCS+)"
    ]
    for ref in nist_refs:
        story.append(Paragraph(ref, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Libraries:</b>", styles['BodyText']))
    libs = [
        "• liboqs 0.15.0 - Open Quantum Safe cryptographic library",
        "• liboqs-python 0.14.1 - Python bindings for liboqs"
    ]
    for lib in libs:
        story.append(Paragraph(lib, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Protocols:</b>", styles['BodyText']))
    protocols = [
        "• KEMTLS: Post-Quantum TLS Without Handshake Signatures (Schwabe et al., 2020)",
        "• OpenID Connect Core 1.0",
        "• OAuth 2.0 Authorization Framework (RFC 6749)",
        "• JSON Web Token (RFC 7519)"
    ]
    for protocol in protocols:
        story.append(Paragraph(protocol, styles['BodyText']))
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    story.append(Paragraph("―" * 50, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Document Version: 1.0 | Last Updated: {datetime.now().strftime('%B %d, %Y')}", 
                          styles['Normal']))
    story.append(Paragraph("For more details, see BenchmarkResults.pdf and source code documentation.",
                          styles['Normal']))
    
    # Build PDF
    print("Building PDF document...")
    doc.build(story)
    
    file_size = os.path.getsize(output_file) / 1024
    print(f"✅ Technical documentation generated: {output_file}")
    print(f"   File size: {file_size:.1f} KB")
    print(f"   Pages: ~{len(story) // 20}")

if __name__ == "__main__":
    try:
        create_technical_documentation()
    except Exception as e:
        print(f"❌ Error generating documentation: {e}")
        import traceback
        traceback.print_exc()
