/**
 * DOM-census heuristics for baseline-url-scan.mjs — detector-only signals
 * that are NOT axe-core rules. Split out of baseline-url-scan.mjs to keep
 * that file within its line budget; imported by --census / --alt-snapshot.
 *
 * Every check here is a heuristic, not a WCAG conformance verdict. Callers
 * must report these under a `census` key, separate from axe's
 * `violations`/`incomplete`, and label findings as detector heuristics that
 * need human triage — never mix them into axe violation counts.
 */

const EMPTY_PARAGRAPH_SAMPLE_LIMIT = 3;

// WCAG 1.3.5 "Input Purposes" known-purpose signals, matched against an
// input's type/name/id/associated-label text. False positives expected: a
// "name" field for a pet, a search box whose placeholder says "email", or
// any non-personal-data field with a coincidental keyword will false-fire —
// this is a triage heuristic for a human to confirm, not a conformance verdict.
const AUTOCOMPLETE_PURPOSE_HINTS = [
  ['name', /\b(full[-_ ]?name|your[-_ ]?name|first[-_ ]?name|last[-_ ]?name)\b/i],
  ['email', /\bemail\b/i],
  ['tel', /\b(tel|phone|mobile)\b/i],
  ['street-address', /\b(street|address([-_ ]?line)?[-_ ]?1|addr1)\b/i],
  ['postal-code', /\b(zip|postal[-_ ]?code)\b/i],
  ['cc-number', /\b(card[-_ ]?number|cc[-_ ]?num(ber)?)\b/i],
  ['cc-name', /\b(card[-_ ]?name|cc[-_ ]?name|name[-_ ]?on[-_ ]?card)\b/i],
];
// Field types where an autocomplete purpose token doesn't meaningfully apply.
const AUTOCOMPLETE_EXCLUDED_TYPES = ['hidden', 'submit', 'button', 'checkbox', 'radio', 'file', 'image', 'reset'];

/**
 * Run the requested census/alt-snapshot checks in-page and return
 * { census, alt_snapshot } — only the requested keys are populated.
 */
export async function collectPageSignals(page, { census = false, altSnapshot = false } = {}) {
  if (!census && !altSnapshot) return {};
  const hints = AUTOCOMPLETE_PURPOSE_HINTS.map(([purpose, re]) => ({ purpose, source: re.source, flags: re.flags }));
  return page.evaluate(
    ({ census, altSnapshot, hints, excludedTypes, paraLimit }) => {
      function selectorFor(el) {
        if (el.id) return `#${CSS.escape(el.id)}`;
        const parts = [];
        let node = el;
        while (node && node.nodeType === 1 && parts.length < 5) {
          let part = node.tagName.toLowerCase();
          const parent = node.parentElement;
          if (parent) {
            const siblings = [...parent.children].filter((c) => c.tagName === node.tagName);
            if (siblings.length > 1) part += `:nth-of-type(${siblings.indexOf(node) + 1})`;
          }
          parts.unshift(part);
          node = parent;
        }
        return parts.join(' > ');
      }

      const out = {};

      if (census) {
        // JS \s already matches non-breaking space, catching the common
        // WYSIWYG "empty paragraph padded with a blank space" pattern.
        const emptyParas = [...document.querySelectorAll('p')].filter(
          (p) => p.children.length === 0 && p.textContent.replace(/\s+/g, '') === ''
        );

        const excluded = new Set(excludedTypes);
        const missingAutocomplete = [];
        for (const field of document.querySelectorAll('input, textarea')) {
          if (field.hasAttribute('autocomplete') || excluded.has(field.type)) continue;
          const label = field.labels?.[0]?.textContent || field.getAttribute('aria-label') || '';
          const signal = [field.type, field.name, field.id, label].join(' ');
          const hit = hints.find((h) => new RegExp(h.source, h.flags).test(signal));
          if (hit) {
            missingAutocomplete.push({ selector: selectorFor(field), purpose: hit.purpose, signal: signal.trim().slice(0, 80) });
          }
        }

        const idGroups = new Map();
        for (const el of document.querySelectorAll('[id]')) {
          const list = idGroups.get(el.id) || [];
          list.push(el.tagName.toLowerCase());
          idGroups.set(el.id, list);
        }
        const duplicateIds = [...idGroups.entries()]
          .filter(([, tags]) => tags.length > 1)
          .map(([id, tags]) => ({ id, count: tags.length, tags }));

        out.census = {
          empty_paragraphs: { count: emptyParas.length, sample_selectors: emptyParas.slice(0, paraLimit).map(selectorFor) },
          autocomplete_absence: { count: missingAutocomplete.length, items: missingAutocomplete },
          duplicate_ids: { count: duplicateIds.length, items: duplicateIds },
        };
      }

      if (altSnapshot) {
        out.alt_snapshot = [...document.querySelectorAll('img, svg[role="img"]')]
          .map((el) => {
            const isImg = el.tagName.toLowerCase() === 'img';
            return {
              selector: selectorFor(el),
              src_or_title: isImg ? el.getAttribute('src') || '' : el.querySelector('title')?.textContent || '',
              alt: isImg ? el.getAttribute('alt') : el.getAttribute('aria-label'),
            };
          })
          .sort((a, b) => a.selector.localeCompare(b.selector));
      }

      return out;
    },
    { census, altSnapshot, hints, excludedTypes: AUTOCOMPLETE_EXCLUDED_TYPES, paraLimit: EMPTY_PARAGRAPH_SAMPLE_LIMIT }
  );
}
