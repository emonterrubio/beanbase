# DESIGN.md — BeanBase Design System

> Version 1.0 | June 2026
> Token names and exact values are placeholders — accent color is coffee brown, not green. Final tokens will be updated when the UI is built.

---

## 1. Brand Identity

### Brand Overview
BeanBase is the intelligence layer for specialty coffee — a platform that surfaces the story behind every cup: where it grew, how it scored, and what it sold for. The brand sits at the intersection of craft and data: credible enough for industry professionals, approachable enough for curious enthusiasts.

### Brand Values
- **Transparency**: Making opaque supply chains legible and navigable
- **Craft**: Deep respect for the skill of producers, importers, and roasters
- **Precision**: Data-first — every claim is sourced, every number is traceable
- **Community**: Built for and with the specialty coffee world, not imposed on it
- **Accessibility**: Pro-grade intelligence without enterprise overhead

### Brand Voice
- **Expert without pretension**: Knows the difference between washed and natural processing; doesn't make you feel bad if you don't
- **Direct**: Data talks — labels are precise, copy is economical
- **Warm**: Coffee is inherently personal; the tone reflects that
- **Curious**: Celebrates discovery — every farm profile is an invitation to explore

### Brand Personality
BeanBase presents itself as a knowledgeable colleague who has spent years in the specialty coffee world: someone who can pull up a Cup of Excellence lot from a 2011 Ethiopian harvest and explain exactly what made it score 92 points. Authoritative on the data side; conversational on the surface.

---

## 2. Color System

> **Note**: Token names use BeanBase-specific nomenclature. Exact hex values for the accent brown will be finalized with the UI. Current values are working approximations tuned for contrast and brand fit.

### Primary Colors

#### Bean Brown (Primary Accent)
```css
--bean-brown: #6F3E1E;
```
- **Usage**: Primary CTAs, active states, links, key data highlights, navigation accents
- **Psychology**: Craft, warmth, earth, coffee origin
- **Accessibility**: Use with white text — verify contrast ratio at final value

#### Dark Roast (Primary Dark)
```css
--dark-roast: #1A0E07;
```
- **Usage**: Primary text, headers, footer backgrounds, sophisticated depth
- **Psychology**: Depth, premium quality, espresso richness
- **Accessibility**: Excellent readability on light backgrounds

### Secondary Colors

#### Honey Gold (Accent)
```css
--honey-gold: #C8913A;
```
- **Usage**: Score highlights, auction price callouts, premium tier indicators, star ratings
- **Psychology**: Value, harvest, warmth, auction prestige

#### Cream (Light Background)
```css
--cream: #F5EDE3;
```
- **Usage**: Card backgrounds, section fills, subtle highlights, origin cards
- **Psychology**: Milk, warmth, approachability

### Neutral Colors

```css
/* Backgrounds */
--white: #FFFFFF;
--warm-white: #FAF8F5;
--cream: #F5EDE3;
--warm-cream: #F0EBE3;

/* Text */
--text-primary: #1A0E07;
--text-secondary: #5C4033;
--text-muted: #8C7066;

/* Borders & Dividers */
--border-light: #E8DDD5;
--border-medium: #D4C4B8;

/* Functional */
--success: #2D7A4F;
--error: #D62B1F;
--warning: #F2A900;
--info: #006DB6;
```

### Color Application

```css
/* Primary Buttons */
.btn-primary {
  background-color: var(--bean-brown);   /* #6F3E1E */
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: var(--dark-roast);   /* #1A0E07 */
}

/* Score/Price Highlights */
.score-badge {
  color: var(--honey-gold);
}

.auction-price {
  color: var(--bean-brown);
  font-weight: 700;
}

/* Card Backgrounds */
.data-card {
  background-color: #FFFFFF;
  border: 1px solid var(--border-light);
}

.origin-card {
  background-color: var(--cream);
}

/* Active Navigation */
.nav__link.active {
  color: var(--bean-brown);
  border-color: var(--bean-brown);
}
```

---

## 3. Typography

### Font Families

#### Primary (UI + Body)
```css
--font-primary: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
```
- **Usage**: Body text, UI labels, navigation, data tables, descriptions
- **Rationale**: Clean, highly legible at small sizes; excellent for data-dense interfaces
- **Weights**: Regular (400), Medium (500), SemiBold (600), Bold (700)

> **Note**: Replace `Inter` with a custom or licensed font when brand identity is finalized. Starbucks uses `SoDo Sans` (proprietary); BeanBase equivalent TBD.

#### Display (Headlines)
```css
--font-display: 'Playfair Display', 'Georgia', serif;
```
- **Usage**: Hero headlines, farm profile names, origin country headers, campaign titles
- **Rationale**: Serif warmth appropriate for a craft/origin brand; evokes quality editorial
- **Weights**: Regular (400), Bold (700)

#### Monospace (Data / API)
```css
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```
- **Usage**: API code samples, lot IDs, score values in data-dense contexts, developer docs

### Type Scale

```css
/* Display */
--text-display-1: 4rem;      /* 64px — Hero headlines */
--text-display-2: 3rem;      /* 48px — Section headers */
--text-display-3: 2.5rem;    /* 40px — Page titles */

/* Headings */
--text-h1: 2rem;             /* 32px */
--text-h2: 1.5rem;           /* 24px */
--text-h3: 1.25rem;          /* 20px */
--text-h4: 1.125rem;         /* 18px */

/* Body */
--text-body-lg: 1.125rem;    /* 18px */
--text-body: 1rem;           /* 16px */
--text-body-sm: 0.875rem;    /* 14px */

/* Small */
--text-caption: 0.75rem;     /* 12px */
--text-overline: 0.6875rem;  /* 11px — uppercase labels */
```

### Typography Styles

```css
/* Farm Profile Title */
.farm-title {
  font-family: var(--font-display);
  font-size: var(--text-display-2);
  font-weight: 700;
  line-height: 1.1;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Section Header */
.section-title {
  font-family: var(--font-primary);
  font-size: var(--text-h1);
  font-weight: 700;
  line-height: 1.25;
  color: var(--dark-roast);
}

/* Lot/Auction Title */
.lot-title {
  font-family: var(--font-primary);
  font-size: var(--text-h3);
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-primary);
}

/* Body Text */
.body-text {
  font-family: var(--font-primary);
  font-size: var(--text-body);
  font-weight: 400;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* Score Display */
.score {
  font-family: var(--font-primary);
  font-size: var(--text-h2);
  font-weight: 700;
  color: var(--honey-gold);
}

/* Price Display */
.price {
  font-family: var(--font-primary);
  font-size: var(--text-body-lg);
  font-weight: 600;
  color: var(--bean-brown);
}

/* Overline Label (e.g., "CUP OF EXCELLENCE") */
.overline {
  font-family: var(--font-primary);
  font-size: var(--text-overline);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* API / Lot ID */
.lot-id {
  font-family: var(--font-mono);
  font-size: var(--text-body-sm);
  color: var(--text-muted);
}
```

---

## 4. Spacing & Layout

### Spacing Scale

```css
--space-0: 0;
--space-1: 0.25rem;    /* 4px */
--space-2: 0.5rem;     /* 8px */
--space-3: 0.75rem;    /* 12px */
--space-4: 1rem;       /* 16px */
--space-5: 1.25rem;    /* 20px */
--space-6: 1.5rem;     /* 24px */
--space-8: 2rem;       /* 32px */
--space-10: 2.5rem;    /* 40px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */
--space-20: 5rem;      /* 80px */
--space-24: 6rem;      /* 96px */
```

### Layout Grid

```css
/* Container */
.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

/* Content Widths */
.content-narrow { max-width: 680px; }
.content-medium { max-width: 960px; }
.content-wide   { max-width: 1200px; }

/* Farm/Lot Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

/* Data Table */
.data-table-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
}
```

### Section Spacing

```css
.section     { padding: var(--space-16) 0; }
.section-lg  { padding: var(--space-24) 0; }

.card        { padding: var(--space-6); }
.card-compact{ padding: var(--space-4); }

.stack-sm    { gap: var(--space-2); }
.stack-md    { gap: var(--space-4); }
.stack-lg    { gap: var(--space-8); }
```

### Breakpoints

```css
--breakpoint-sm:  375px;   /* Mobile */
--breakpoint-md:  768px;   /* Tablet */
--breakpoint-lg:  1024px;  /* Desktop */
--breakpoint-xl:  1280px;  /* Large Desktop */
--breakpoint-2xl: 1440px;  /* Extra Large */
```

---

## 5. Component Library

### Buttons

```css
/* Primary — Bean Brown */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.5rem;
  font-family: var(--font-primary);
  font-size: 1rem;
  font-weight: 600;
  color: #FFFFFF;
  background-color: var(--bean-brown);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--dark-roast);
  transform: scale(1.02);
}

/* Secondary — Outline */
.btn-secondary {
  padding: 0.875rem 1.5rem;
  font-family: var(--font-primary);
  font-size: 1rem;
  font-weight: 600;
  color: var(--bean-brown);
  background-color: transparent;
  border: 2px solid var(--bean-brown);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: var(--bean-brown);
  color: #FFFFFF;
}

/* Ghost */
.btn-ghost {
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: var(--bean-brown);
  background: transparent;
  border: none;
  cursor: pointer;
}

.btn-ghost:hover {
  text-decoration: underline;
}
```

### Farm / Lot Cards

```css
.data-card {
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-light);
  box-shadow: 0 1px 3px rgba(26, 14, 7, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.data-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(26, 14, 7, 0.12);
}

.data-card__header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-light);
}

.data-card__overline {
  font-size: var(--text-overline);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: var(--space-1);
}

.data-card__title {
  font-size: var(--text-h4);
  font-weight: 600;
  color: var(--text-primary);
}

.data-card__body {
  padding: var(--space-4);
  flex: 1;
}

.data-card__footer {
  padding: var(--space-3) var(--space-4);
  background: var(--warm-white);
  border-top: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Score Badge

```css
/* Auction Score Display */
.score-badge {
  display: inline-flex;
  align-items: baseline;
  gap: var(--space-1);
}

.score-badge__value {
  font-size: var(--text-h2);
  font-weight: 700;
  color: var(--honey-gold);
  font-family: var(--font-primary);
}

.score-badge__label {
  font-size: var(--text-caption);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Score color bands */
.score--exceptional { color: #B8860B; }   /* 90+ */
.score--outstanding { color: var(--honey-gold); } /* 87–89 */
.score--excellent   { color: #C8913A; }   /* 85–86 */
```

### Origin Intelligence Card

```css
.origin-card {
  background: var(--cream);
  border-radius: 12px;
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

.origin-card__country {
  font-family: var(--font-display);
  font-size: var(--text-h1);
  font-weight: 700;
  color: var(--dark-roast);
  margin-bottom: var(--space-2);
}

.origin-card__region {
  font-size: var(--text-body-sm);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: var(--space-4);
}

.origin-card__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.origin-stat__value {
  font-size: var(--text-h3);
  font-weight: 700;
  color: var(--bean-brown);
}

.origin-stat__label {
  font-size: var(--text-caption);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
```

### Certification Badge

```css
.cert-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: var(--text-caption);
  font-weight: 600;
  background: var(--warm-cream);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.cert-badge--fair-trade  { background: #FFF3CD; color: #7A5000; }
.cert-badge--rainforest  { background: #D4EDD9; color: #1C5E2B; }
.cert-badge--organic     { background: #E8F4E8; color: #2E5E2E; }
.cert-badge--bird-friendly { background: #E8F0FB; color: #1A3A6B; }
```

### Data Table (Auction Results)

```css
.auction-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-body-sm);
}

.auction-table th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: var(--text-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  border-bottom: 2px solid var(--border-medium);
}

.auction-table td {
  padding: var(--space-3) var(--space-4);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.auction-table tr:hover td {
  background: var(--warm-white);
}

.auction-table .score-col {
  font-weight: 700;
  color: var(--honey-gold);
}

.auction-table .price-col {
  font-weight: 600;
  color: var(--bean-brown);
}
```

### Navigation

```css
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: #FFFFFF;
  box-shadow: 0 1px 3px rgba(26, 14, 7, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav__links {
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

.nav__link {
  font-family: var(--font-primary);
  font-size: var(--text-body);
  font-weight: 600;
  color: var(--text-primary);
  text-decoration: none;
  padding: var(--space-2) 0;
  border-bottom: 2px solid transparent;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.nav__link:hover {
  color: var(--bean-brown);
  border-color: var(--bean-brown);
}

.nav__link.active {
  color: var(--bean-brown);
  border-color: var(--bean-brown);
}
```

### Search Bar

```css
.search-bar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: #FFFFFF;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-bar:focus-within {
  border-color: var(--bean-brown);
  box-shadow: 0 0 0 3px rgba(111, 62, 30, 0.12);
}

.search-bar__input {
  flex: 1;
  border: none;
  outline: none;
  font-size: var(--text-body);
  color: var(--text-primary);
  background: transparent;
}

.search-bar__input::placeholder {
  color: var(--text-muted);
}
```

### Filter Chip

```css
.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 0.375rem 0.75rem;
  border: 1.5px solid var(--border-medium);
  border-radius: 50px;
  font-size: var(--text-body-sm);
  font-weight: 500;
  color: var(--text-secondary);
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-chip:hover {
  border-color: var(--bean-brown);
  color: var(--bean-brown);
}

.filter-chip.active {
  background: var(--bean-brown);
  border-color: var(--bean-brown);
  color: #FFFFFF;
}
```

---

## 6. Iconography

### Icon Style Guidelines
- **Style**: Clean, minimal, consistent weight — data-forward, not decorative
- **Stroke Width**: 1.5px for standard; 2px for interactive icons
- **Corners**: Slightly rounded — approachable without being childish
- **Size**: 24px base

### Core Icons

```
Navigation:
[=]   Menu
[<-]  Back
[X]   Close
[v]   Chevron down
[>]   Chevron right
[🔍]  Search

Data / Coffee:
[☕]  Coffee/origin
[🌍]  Map/region
[📊]  Chart/price trend
[🏆]  Award/auction result
[📋]  Lot detail
[🌱]  Farm/growing
[📅]  Harvest calendar

Certifications:
[✓]   Certified
[🌿]  Organic / Rainforest
[⭐]  Score / Rating

Actions:
[↓]   Export / Download
[↗]   Share
[🔔]  Alert / Notify
[+]   Add to watchlist
[♡]   Save / Favorite

Account:
[👤]  Profile
[💳]  Billing
[🔑]  API key
[⚙]   Settings
```

### Icon Sizes

```css
--icon-xs: 16px;   /* Inline indicators, badges */
--icon-sm: 20px;   /* Compact UI, table rows */
--icon-md: 24px;   /* Default */
--icon-lg: 32px;   /* Feature icons */
--icon-xl: 48px;   /* Hero / empty states */
```

---

## 7. Motion & Animation

### Animation Principles
- **Data-first**: Transitions serve comprehension — charts animate in meaningfully, not decoratively
- **Purposeful**: Micro-interactions confirm actions and guide attention
- **Restrained**: This is a data product; motion should not compete with information
- **Fast**: Snappy interactions that respect user time

### Timing Values

```css
--duration-instant: 100ms;   /* Micro-interactions */
--duration-fast:    200ms;   /* Buttons, toggles, chips */
--duration-normal:  300ms;   /* Cards, panels */
--duration-slow:    400ms;   /* Page transitions, modals */
--duration-chart:   600ms;   /* Chart/graph entrance */
```

### Easing Curves

```css
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-in:      cubic-bezier(0.4, 0, 1, 1);
--ease-out:     cubic-bezier(0, 0, 0.2, 1);
--ease-bounce:  cubic-bezier(0.34, 1.56, 0.64, 1);
```

### Component Animations

```css
/* Card hover lift */
.data-card {
  transition: transform var(--duration-normal) var(--ease-out),
              box-shadow var(--duration-normal) var(--ease-out);
}
.data-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(26, 14, 7, 0.12);
}

/* Button press */
.btn-primary:active { transform: scale(0.98); }

/* Score/price chart entrance */
@keyframes chartLine {
  from { stroke-dashoffset: 100%; opacity: 0; }
  to   { stroke-dashoffset: 0;    opacity: 1; }
}
.chart-line { animation: chartLine var(--duration-chart) var(--ease-out); }

/* Page fade */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page-enter { animation: fadeIn var(--duration-normal) var(--ease-out); }

/* Skeleton loading */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}
.skeleton {
  background: linear-gradient(
    90deg,
    var(--warm-cream) 25%,
    var(--border-light) 50%,
    var(--warm-cream) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

/* Modal slide-up */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(100%); }
  to   { opacity: 1; transform: translateY(0); }
}
.modal-enter { animation: slideUp var(--duration-slow) var(--ease-out); }

/* Reduced motion override */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
  .data-card:hover { transform: none; }
}
```

---

## 8. Accessibility

### Color Contrast Targets

| Combination | Target WCAG |
|-------------|-------------|
| White on Bean Brown (#6F3E1E) | AA (4.5:1+) — verify at final value |
| White on Dark Roast (#1A0E07) | AAA (11:1+) |
| Dark Roast on White | AAA |
| Bean Brown on White | AA |
| Honey Gold on Dark Roast | AA |
| Text Secondary on White | AAA |

> Verify all contrast ratios against final hex values using WebAIM Contrast Checker before shipping.

### Focus States

```css
*:focus-visible {
  outline: 2px solid var(--bean-brown);
  outline-offset: 2px;
}

.btn:focus-visible {
  outline: 3px solid var(--bean-brown);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(111, 62, 30, 0.2);
}

.input:focus {
  border-color: var(--bean-brown);
  box-shadow: 0 0 0 3px rgba(111, 62, 30, 0.15);
}
```

### Touch Targets

```css
/* Minimum 44×44px touch target */
.btn, .nav__link, .filter-chip, .data-card { min-height: 44px; }
```

### Screen Reader Support

```html
<!-- Auction score -->
<div aria-label="Score: 92.5 points">
  <span aria-hidden="true">92.5</span>
  <span class="sr-only">points</span>
</div>

<!-- Farm card -->
<article aria-labelledby="farm-name-123" role="button" tabindex="0">
  <h3 id="farm-name-123">Finca La Palma</h3>
  <p>Ethiopia · Yirgacheffe · Washed</p>
</article>

<!-- Filter group -->
<fieldset>
  <legend>Filter by origin</legend>
  <label><input type="checkbox" value="ethiopia"> Ethiopia</label>
  <label><input type="checkbox" value="kenya"> Kenya</label>
</fieldset>

<!-- Live region for search results -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  24 farms found for "Ethiopia"
</div>
```

---

## 9. Responsive Patterns

### Mobile-First Data Grid

```css
/* Mobile default: 1 column */
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop: 3–4 columns */
@media (min-width: 1024px) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1280px) {
  .card-grid { grid-template-columns: repeat(4, 1fr); }
}
```

### Data Table (Mobile Collapse)

```css
/* On mobile, auction tables collapse to card view */
@media (max-width: 767px) {
  .auction-table thead { display: none; }

  .auction-table tr {
    display: block;
    padding: var(--space-4);
    border: 1px solid var(--border-light);
    border-radius: 8px;
    margin-bottom: var(--space-3);
  }

  .auction-table td {
    display: flex;
    justify-content: space-between;
    border-bottom: none;
    padding: var(--space-1) 0;
  }

  .auction-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--text-muted);
    font-size: var(--text-caption);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
}
```

---

## 10. Data Visualization

### Chart Color Palette

For score trend lines, price charts, origin comparisons:

```css
/* Ordered by visual priority */
--chart-1: #6F3E1E;   /* Bean Brown — primary series */
--chart-2: #C8913A;   /* Honey Gold — secondary series */
--chart-3: #2D7A4F;   /* Forest Green — tertiary series */
--chart-4: #4A7BA8;   /* Steel Blue */
--chart-5: #8B5E8B;   /* Purple */
--chart-6: #C0564A;   /* Rust Red */
```

### Score Band Coloring

```css
/* Used in auction result tables and charts */
.score-band--90plus  { color: #B8860B; background: #FFF8E7; }   /* 90+ Exceptional */
.score-band--87to89  { color: #C8913A; background: #FFF4E0; }   /* 87–89 Outstanding */
.score-band--85to86  { color: #6F3E1E; background: #F9EEE6; }   /* 85–86 Excellent */
.score-band--below85 { color: var(--text-muted); background: var(--warm-white); }
```

---

## Appendix: Quick Reference

### Color Tokens
```
Primary:       --bean-brown:   #6F3E1E  (CTA, active states)
Dark:          --dark-roast:   #1A0E07  (text, footer bg)
Accent:        --honey-gold:   #C8913A  (scores, prices)
Background:    --cream:        #F5EDE3  (cards, origin sections)
Text Primary:  --text-primary: #1A0E07
Text Muted:    --text-muted:   #8C7066
```

### Font Stack
```
Primary:  Inter, Helvetica Neue, Arial, sans-serif
Display:  Playfair Display, Georgia, serif
Mono:     JetBrains Mono, Fira Code, Courier New, monospace
```

### Core Spacing
```
4px | 8px | 12px | 16px | 24px | 32px | 48px | 64px
```

### Border Radius
```
Small:    4px  (chips, badges)
Medium:   8px  (cards, inputs)
Large:    12px (origin cards)
Full:     50px (filter pills)
```

### Breakpoints
```
Mobile:   375px
Tablet:   768px
Desktop:  1024px
Large:    1280px
XL:       1440px
```

### Z-Index Scale
```
Dropdown: 100
Sticky:   200
Modal:    300
Toast:    400
Tooltip:  500
```

---

*BeanBase Design System v1.0 | June 2026*
*Token names and hex values for the accent brown are working approximations — update when UI is finalized.*
