import re

bilingual_file = '/Users/souvikbasu/Downloads/Grow Global/growinvoice-main/growinvoice_bilingual_landing.html'
with open(bilingual_file, 'r') as f:
    landing_html = f.read()

# Extract fonts
fonts_match = re.search(r'<link href="https://fonts\.googleapis\.com.*?">', landing_html)
fonts = fonts_match.group(0) if fonts_match else ''

# Extract styles
styles_match = re.search(r'<style>.*?</style>', landing_html, re.DOTALL)
styles = styles_match.group(0) if styles_match else ''

# Extract body sections between <!-- HERO --> and <footer>
body_match = re.search(r'(<!-- HERO -->.*?)<footer', landing_html, re.DOTALL)
body = body_match.group(1).strip() if body_match else ''

# Extract scripts
scripts_match = re.search(r'<script>.*?</script>', landing_html, re.DOTALL)
scripts = scripts_match.group(0) if scripts_match else ''

new_index = f"""@@include('header.htm')

@@include('components/meta-keywords.htm')

<!-- Performance Optimization Meta Tags -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://www.youtube.com">
<link rel="dns-prefetch" href="https://www.youtube.com">
<link rel="preload" href="images/payment/digital-currency.png" as="image">
<link rel="preload" href="images/payment/invoice.png" as="image">
<link rel="preload" href="images/payment/tax.png" as="image">
{fonts}

{styles}

<style>
  .lazy-iframe {{
    background: #f0f0f0;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-size: 14px;
  }}
  
  .lazy-iframe::before {{
    content: "Loading video...";
  }}
  
  img[loading="lazy"] {{
    transition: opacity 0.3s ease;
  }}
  
  img[loading="lazy"]:not([src]) {{
    opacity: 0;
  }}
</style>

@@include('components/navbar-inner.htm',{{
  "nav": "",
}})

{body}

@@include('components/footer.htm')

@@include('footer.htm')

{scripts}

<!-- Lazy Loading Enhancement Script -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
  // Lazy load iframes
  const lazyIframes = document.querySelectorAll('.lazy-iframe');
  
  if ('IntersectionObserver' in window) {{
    const iframeObserver = new IntersectionObserver((entries, observer) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          const iframe = entry.target;
          iframe.src = iframe.dataset.src;
          iframe.classList.remove('lazy-iframe');
          observer.unobserve(iframe);
        }}
      }});
    }}, {{
      rootMargin: '50px 0px',
      threshold: 0.1
    }});
    
    lazyIframes.forEach(iframe => {{
      iframeObserver.observe(iframe);
    }});
  }} else {{
    // Fallback for older browsers
    lazyIframes.forEach(iframe => {{
      iframe.src = iframe.dataset.src;
    }});
  }}
  
  // Preload critical images on hover
  const criticalImages = document.querySelectorAll('img[loading="lazy"]');
  criticalImages.forEach(img => {{
    img.addEventListener('mouseenter', function() {{
      if (!this.complete) {{
        this.loading = 'eager';
      }}
    }}, {{ once: true }});
  }});
}});
</script>
"""

with open('/Users/souvikbasu/Downloads/Grow Global/growinvoice-main/src/index.html', 'w') as f:
    f.write(new_index)

print("Done generating new index.html")
