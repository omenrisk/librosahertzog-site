#!/usr/bin/env python3
"""Genera /libros/index.html (ES) y /en/index.html (EN) desde una sola tabla.

Uso:  python3 build_catalog.py
La tabla BOOKS es la fuente de verdad de la biblioteca de seguridad en la web:
ASINs, portadas (assets/covers/*.jpg, 360 px) y una línea por libro.
Solo libros de seguridad + la app (decisión de Luis, 21-sep-2026).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TAG = "librosahertzo-20"
AUTHOR_STORE = f"https://www.amazon.com/stores/author/B0F2D8RVZ7?tag={TAG}"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdGaKHEBHmJ42g_p61_QE7B7nEWvr30d_mfI89CKDZb9dw61Q/viewform"


def amz(asin):
    return f"https://www.amazon.com/dp/{asin}?tag={TAG}"


# (cover, kindle ASIN, papel ASIN, título, subtítulo/una línea)
ES = [
    ("es_analisis", "B07WDYQ62F", "1733773134", "Análisis de Riesgo",
     "Método cuantitativo, contramedidas y mitigación. El más vendido de la serie."),
    ("es_riesgo", "B0GX2XB7VR", "B0GZDGLB3F", "RIESGO: De la Matriz a la Decisión",
     "Cómo se decide cuando los números no alcanzan."),
    ("es_fundamentos", "B0GWYRYBWY", "B0GX1WQ644", "Fundamentos de la Investigación Criminal",
     "El porqué: ética, sesgos y evidencia. Empieza aquí."),
    ("es_manual", "B0GNNBYFQ4", "B0GNS27JRQ", "Manual del Investigador de Seguridad Corporativa",
     "El cómo: protocolos, escena y entrevistas en 16 capítulos."),
    ("es_investigaciones", "B0812597D2", "1733773150", "Investigaciones e Interrogatorios",
     "La entrevista como herramienta de trabajo."),
    ("es_cpp_psp", "B0GNXNFDY2", "B0GNZN5LD4", "CPP y PSP — 1,000 Preguntas",
     "El banco completo con respuestas comentadas, en papel y Kindle."),
]

EN = [
    ("en_risk_analysis", "B0GX33FYHB", "B0HHYBFW9N", "Risk Analysis",
     "Quantitative Method, Countermeasures and Mitigation."),
    ("en_risk", "B0HJ12W4FF", "B0HHZY9D3L", "Risk",
     "From the Matrix to the Decision."),
    ("en_fundamentals", "B0HHZWS8BV", "B0HHXK5NYP", "Fundamentals of Criminal Investigation",
     "Science, Method and Judgment."),
    ("en_manual", "B0HJ18LW7V", "B0HJ2FVNJZ", "Corporate Security Investigator's Manual",
     "Protocols, scene management and interviews for workplace investigations."),
    ("en_interviews", "B0H2G1BJRG", "B0HJ1GBKZ9", "Interviews and Interrogations",
     "Reid, PEACE and WZ compared: the interview as a working tool."),
    ("en_cpp_psp", "B0HJFXTQM7", "B0HJHH6YJD", "CPP and PSP: Practice Question Bank",
     "1,000 Questions and Detailed Answers."),
]

CSS = """
  :root{--navy:#0d1b2e;--ink:#1c2733;--silver:#c7d0dc;--gold:#f0c05a;--blue:#6ec8ff;--bg:#f6f8fa}
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
  .topbar{background:#0b2545;color:#fff;text-align:center;padding:10px 16px;font-size:15px}
  .topbar a{color:#ffd166;font-weight:bold}
  .hero{background:linear-gradient(180deg,#0d1b2e 0%,#0a1424 100%);color:#fff;text-align:center;padding:44px 20px 40px;position:relative}
  .brand{letter-spacing:.35em;font-size:.8rem;color:var(--silver);text-transform:uppercase;margin-bottom:14px}
  .hero h1{font-size:clamp(1.5rem,4.5vw,2.4rem);font-weight:800;line-height:1.25;margin-bottom:12px}
  .hero p{max-width:600px;margin:0 auto 22px;color:var(--silver);font-size:1.05rem}
  .lang{position:absolute;top:12px;right:14px;font-size:.85rem}
  .lang a{color:var(--blue);text-decoration:none;border:1px solid rgba(110,200,255,.5);padding:4px 10px;border-radius:999px}
  .btn{display:inline-block;padding:13px 26px;border-radius:8px;font-weight:700;text-decoration:none;font-size:1rem;margin:6px}
  .btn-gold{background:var(--gold);color:var(--navy)}
  .btn-outline{border:2px solid var(--blue);color:var(--blue)}
  .btn:hover{opacity:.9}
  section{max-width:960px;margin:0 auto;padding:40px 22px 8px}
  h2{color:var(--navy);font-size:1.35rem;margin-bottom:6px;border-bottom:3px solid var(--gold);display:inline-block;padding-bottom:4px}
  .lead{color:#4a5a6a;margin-bottom:18px;font-size:.98rem}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
  .book{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px;box-shadow:0 1px 4px rgba(13,27,46,.06);display:flex;gap:14px;align-items:flex-start}
  .book img{width:88px;height:auto;border-radius:4px;flex:0 0 auto;box-shadow:0 2px 8px rgba(13,27,46,.25)}
  .book h3{color:var(--navy);font-size:1rem;line-height:1.3;margin-bottom:4px}
  .book p{font-size:.88rem;color:#4a5a6a;margin-bottom:10px}
  .book .fmt a{display:inline-block;font-size:.82rem;font-weight:700;text-decoration:none;padding:7px 12px;border-radius:7px;margin:0 6px 6px 0}
  .book .k{background:var(--navy);color:#fff}
  .book .p{border:1.5px solid var(--navy);color:var(--navy)}
  .bio p{margin-bottom:14px}
  .sello{font-weight:600}
  .app{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:24px;text-align:center;box-shadow:0 1px 4px rgba(13,27,46,.06);max-width:560px;margin:0 auto}
  .app .emoji{font-size:2rem;margin-bottom:8px}
  .app h3{color:var(--navy);font-size:1.05rem;margin-bottom:8px}
  .app p{font-size:.92rem;color:#4a5a6a;margin-bottom:16px}
  .app a{display:inline-block;background:var(--navy);color:#fff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:.92rem}
  .more{text-align:center;margin:18px 0 0;font-size:.92rem}
  .more a{color:#33689c}
  footer{background:var(--navy);color:var(--silver);text-align:center;padding:26px 20px;font-size:.88rem;margin-top:40px}
  footer a{color:var(--blue);text-decoration:none}
  .fine{font-size:.78rem;opacity:.75;display:block;margin-top:6px}
"""


def card(cover, kindle, paper, title, line, k_label, p_label):
    return f"""    <div class="book">
      <img src="/assets/covers/{cover}.jpg" alt="{title}" loading="lazy" width="88">
      <div>
        <h3>{title}</h3>
        <p>{line}</p>
        <div class="fmt"><a class="k" href="{amz(kindle)}">{k_label}</a><a class="p" href="{amz(paper)}">{p_label}</a></div>
      </div>
    </div>"""


def grid(books, k_label, p_label):
    return '  <div class="grid">\n' + "\n".join(card(*b, k_label, p_label) for b in books) + "\n  </div>"


HREFLANG = """<link rel="alternate" hreflang="es" href="https://librosahertzog.com/libros/">
<link rel="alternate" hreflang="en" href="https://librosahertzog.com/en/">
<link rel="alternate" hreflang="x-default" href="https://librosahertzog.com/libros/">"""

FOOTER_ES = """<footer>
  Contacto: <a href="mailto:info@librosahertzog.com">info@librosahertzog.com</a><br>
  © 2026 A. Hertzog · EXPERTO EN SEGURIDAD
  <span class="fine">Como Asociado de Amazon, percibimos ingresos por las compras adscritas que cumplen los requisitos aplicables.</span>
  <span class="fine">App y libros de estudio independientes. CPP® y PSP® son marcas registradas de ASIS International, Inc. Este sitio no está afiliado a ASIS International ni patrocinado o avalado por ella; toda referencia es puramente descriptiva.</span>
</footer>"""

FOOTER_EN = """<footer>
  Contact: <a href="mailto:info@librosahertzog.com">info@librosahertzog.com</a><br>
  © 2026 A. Hertzog · SECURITY EXPERT
  <span class="fine">As an Amazon Associate we earn from qualifying purchases.</span>
  <span class="fine">Independent study books and app. CPP® and PSP® are registered certification marks of ASIS International, Inc. This site is not affiliated with, sponsored or endorsed by ASIS International; any reference is purely descriptive.</span>
</footer>"""

ES_PAGE = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>La biblioteca completa — Experto en Seguridad | A. Hertzog</title>
<meta name="description" content="Los doce libros de seguridad de A. Hertzog: seis en español (serie EXPERTO EN SEGURIDAD) y sus seis U.S. Editions en inglés. Riesgo, investigación, entrevistas y preparación CPP/PSP. Papel y Kindle en Amazon.">
<link rel="canonical" href="https://librosahertzog.com/libros/">
{HREFLANG}
<meta property="og:title" content="La biblioteca completa — Experto en Seguridad">
<meta property="og:description" content="Seis libros en español y seis U.S. Editions en inglés. Papel y Kindle en Amazon.">
<meta property="og:url" content="https://librosahertzog.com/libros/">
<meta property="og:type" content="website">
<style>{CSS}</style>
</head>
<body>

<div class="topbar">
  📱 Seguridad Pro: CPP &amp; PSP — 10 preguntas gratis cada día, en iPhone y Android —
  <a href="/app/?utm_source=site&amp;utm_medium=banner&amp;utm_campaign=biblioteca">pruébala →</a>
</div>

<div class="hero">
  <div class="lang"><a href="/en/" hreflang="en" lang="en">English</a></div>
  <div class="brand">Experto en Seguridad</div>
  <h1>La biblioteca completa</h1>
  <p>Seis libros en español y sus seis ediciones en inglés (U.S. Editions). Riesgo, investigación, entrevistas e interrogatorios y preparación CPP/PSP. En papel y Kindle, en Amazon.</p>
  <a class="btn btn-gold" href="#espanol">Los libros en español</a>
  <a class="btn btn-outline" href="#english">In English</a>
</div>

<section id="espanol">
  <h2>Serie EXPERTO EN SEGURIDAD · en español</h2>
  <p class="lead">Seis libros, del método al criterio. Cada uno se lee solo; juntos son el oficio completo.</p>
{grid(ES, "Kindle", "Tapa blanda")}
</section>

<section id="english" lang="en">
  <h2>SECURITY EXPERT series · U.S. Editions</h2>
  <p class="lead">The same six books, rewritten for the U.S. reader by the author. Paperback and Kindle on Amazon.com.</p>
{grid(EN, "Kindle", "Paperback")}
  <p class="more"><a href="/en/">Read about the series in English →</a></p>
</section>

<section>
  <h2>La app</h2>
  <p class="lead">El banco de 1,000 preguntas del libro de CPP y PSP, en tu bolsillo.</p>
  <div class="app">
    <div class="emoji">📱</div>
    <h3>Seguridad Pro: CPP &amp; PSP</h3>
    <p>1,000 preguntas con explicación y trampa típica, simulacros a ritmo real y repaso automático de errores. Interfaz en español e inglés. 10 preguntas gratis cada día; el desbloqueo es un pago único, sin suscripción. iPhone y Android.</p>
    <a href="/app/?utm_source=site&amp;utm_medium=card&amp;utm_campaign=biblioteca">Descargar la app</a>
  </div>
  <p class="more"><a href="{AUTHOR_STORE}">Página de autor en Amazon</a> · <a href="/links/">Todos los enlaces</a> · <a href="/">Inicio</a></p>
</section>

{FOOTER_ES}

</body>
</html>
"""

EN_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Expert — U.S. Editions by A. Hertzog | Books and CPP · PSP prep app</title>
<meta name="description" content="Six books on security risk analysis, corporate investigations, interviewing and CPP/PSP exam prep, written by a practitioner. U.S. Editions in paperback and Kindle, plus the Security Pro app with 1,000 explained questions.">
<link rel="canonical" href="https://librosahertzog.com/en/">
{HREFLANG}
<meta property="og:title" content="Security Expert — U.S. Editions by A. Hertzog">
<meta property="og:description" content="Six books on security risk, investigations and interviewing, plus the CPP/PSP prep app.">
<meta property="og:url" content="https://librosahertzog.com/en/">
<meta property="og:type" content="website">
<style>{CSS}</style>
</head>
<body>

<div class="topbar">
  📱 Security Pro: CPP &amp; PSP Prep — 10 free questions a day, on iPhone and Android —
  <a href="https://apps.apple.com/app/security-pro-cpp-psp-prep/id6794937345">App Store</a> ·
  <a href="https://play.google.com/store/apps/details?id=com.luispalma.seguridadpro&amp;referrer=utm_source%3Dlibrosahertzog%26utm_medium%3Den_home%26utm_campaign%3Dus_editions">Google Play</a>
</div>

<div class="hero">
  <div class="lang"><a href="/libros/" hreflang="es" lang="es">Español</a></div>
  <div class="brand">Security Expert</div>
  <h1>Security books written by a practitioner, not a committee.</h1>
  <p>Six U.S. Editions on risk analysis, corporate investigations, interviewing and CPP/PSP exam preparation. Method first, judgment always. Paperback and Kindle on Amazon.com.</p>
  <a class="btn btn-gold" href="#books">See the six books</a>
  <a class="btn btn-outline" href="#app">The prep app</a>
</div>

<section class="bio">
  <h2>About the author</h2>
  <p>Luis Palma is a security professional with operational and management experience. He served in the U.S. Marine Corps, worked in police functions and currently coordinates security programs in the region. He holds a Bachelor's in Criminal Justice and keeps up continuing education on a recurring basis.</p>
  <p class="sello">He publishes the <strong>SECURITY EXPERT</strong> series under the <strong>A.&nbsp;Hertzog</strong> imprint.</p>
</section>

<section id="books">
  <h2>The six U.S. Editions</h2>
  <p class="lead">Each book stands on its own; together they cover the trade from method to decision.</p>
{grid(EN, "Kindle", "Paperback")}
</section>

<section id="app">
  <h2>The app</h2>
  <p class="lead">The 1,000-question bank from the CPP and PSP book, in your pocket.</p>
  <div class="app">
    <div class="emoji">📱</div>
    <h3>Security Pro: CPP &amp; PSP Prep</h3>
    <p>1,000 practice questions, each with an explanation and the common trap; timed mock exams at real exam pace; automatic error review. Interface in English and Spanish. 10 free questions every day; unlock everything with a single one-time purchase, no subscription. 100% offline.</p>
    <a href="https://apps.apple.com/app/security-pro-cpp-psp-prep/id6794937345">App Store</a>&nbsp;
    <a href="https://play.google.com/store/apps/details?id=com.luispalma.seguridadpro&amp;referrer=utm_source%3Dlibrosahertzog%26utm_medium%3Den_card%26utm_campaign%3Dus_editions">Google Play</a>
  </div>
</section>

<section id="espanol" lang="es">
  <h2>Serie EXPERTO EN SEGURIDAD · en español</h2>
  <p class="lead">The original Spanish series, also on Amazon.</p>
{grid(ES, "Kindle", "Tapa blanda")}
  <p class="more"><a href="{AUTHOR_STORE}">Author page on Amazon</a> · <a href="/libros/">La biblioteca en español →</a></p>
</section>

{FOOTER_EN}

</body>
</html>
"""

if __name__ == "__main__":
    for rel, html in (("libros/index.html", ES_PAGE), ("en/index.html", EN_PAGE)):
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"{rel}: {len(html.encode())} bytes")
