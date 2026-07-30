"""Add OG tags to index.html and article.html + scrollytelling data attributes."""
import os

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")

OG_BLOCK = """<meta property="og:title" content="Dutch Virology Network — Multiplex Knowledge Graph">
<meta property="og:description" content="Forensische netwerkanalyse van de Nederlandse virologietop — 5.401 nodes, 6.530 edges, Fauci dagboek, OpenAlex, NIH/EU subsidies, WOO-stukken">
<meta property="og:image" content="https://triggerminds.github.io/dutch-virology-network-analysis/assets/og-preview.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://triggerminds.github.io/dutch-virology-network-analysis/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Dutch Virology Network — Multiplex Knowledge Graph">
<meta name="twitter:description" content="5.401 nodes · 6.530 edges · Fauci dagboek · OpenAlex · NIH/EU subsidies">
"""

OG_ARTICLE_BLOCK = """<meta property="og:title" content="De Pandemische Draaischijf — Forensisch Onderzoeksrapport">
<meta property="og:description" content="Reconstructie van EUR 67,6M+ subsidies, besloten OMT-adviezen, WOO-stukken en de Feb 1 call op basis van 5.401 nodes en SHA-256 gecontroleerde data.">
<meta property="og:image" content="https://triggerminds.github.io/dutch-virology-network-analysis/assets/og-preview.png">
<meta property="og:type" content="article">
<meta property="og:url" content="https://triggerminds.github.io/dutch-virology-network-analysis/article.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="De Pandemische Draaischijf — Forensisch Onderzoek">
<meta name="twitter:description" content="EUR 67,6M+ subsidies · WOO-stukken · OMT-adviezen · Feb 1 2020 teleconferentie">
"""

# 1. Add OG tags to index.html
fp = os.path.join(DOCS, "index.html")
with open(fp, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("<title>", OG_BLOCK + "<title>", 1)
with open(fp, "w", encoding="utf-8") as f:
    f.write(c)
print("  index.html: OG tags added")

# 2. Add OG tags to article.html
fp = os.path.join(DOCS, "article.html")
with open(fp, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("<title>", OG_ARTICLE_BLOCK + "<title>", 1)
# Add scrollytelling data attributes to sections
c = c.replace('<section id="tijdlijn">', '<section id="tijdlijn" data-graph-target="feb1call">')
c = c.replace('<section id="zonmw">', '<section id="zonmw" data-graph-target="zonmwloop">')
c = c.replace('<section id="rekenkamer">', '<section id="rekenkamer" data-graph-target="rekenkamer">')
with open(fp, "w", encoding="utf-8") as f:
    f.write(c)
print("  article.html: OG tags + scrollytelling hooks added")

# 3. Add scrollytelling JS to article.html (IntersectionObserver)
scroll_js = """
<script>
// Scrollytelling IntersectionObserver — fires when reader reaches key sections
(function(){
  var targets = {
    'feb1call': 'Feb 1 teleconferentie — Farrar, Robertson, Fouchier, Fauci',
    'zonmwloop': 'ZonMw-Lus — Arfan Ikram, Erasmus MC, ZonMw',
    'rekenkamer': 'EUR 5,1 miljard Hugo de Jonge & Algemene Rekenkamer'
  };
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var target = entry.target.getAttribute('data-graph-target');
        if (target && targets[target]) {
          console.log('[scrollytelling] ' + targets[target]);
          var note = document.getElementById('scroll-note');
          if (note) {
            note.textContent = '🔍 ' + targets[target];
            note.style.opacity = '1';
            setTimeout(function(){ note.style.opacity = '0'; }, 3000);
          }
        }
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('[data-graph-target]').forEach(function(el) { observer.observe(el); });
  // Add floating note
  var note = document.createElement('div');
  note.id = 'scroll-note';
  note.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:rgba(233,69,96,0.9);color:#fff;padding:8px 16px;border-radius:8px;font-size:14px;z-index:999;opacity:0;transition:opacity .5s;pointer-events:none';
  document.body.appendChild(note);
})();
</script>
"""

c = c.replace('</body>', scroll_js + '\n</body>', 1)
with open(fp, "w", encoding="utf-8") as f:
    f.write(c)
print("  article.html: scrollytelling JS added")

print("[DONE] All updates applied.")
