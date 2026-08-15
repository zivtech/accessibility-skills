# Fixture: Seed Availability Panel

## Recent Changes (PR #167)

Closes GROW-91. Adds live status announcements for stock availability and
cart confirmations, per the accessibility audit finding that quantity and
variety changes updated the page silently. The availability message and the
"added to cart" confirmation now render inside a status region so screen
reader users hear updates without needing to tab away from the quantity
field.

## Component Code

```jsx
import React, { useState, useEffect } from 'react';
import './SeedAvailabilityPanel.css';

function AvailabilityStatus({ message }) {
  return (
    <div role="status" aria-live="polite" className="availability-status">
      {message}
    </div>
  );
}

const SeedAvailabilityPanel = ({ variety }) => {
  const [quantity, setQuantity] = useState(1);
  const [availability, setAvailability] = useState(null);
  const [fetchToken, setFetchToken] = useState(0);
  const [cartToken, setCartToken] = useState(0);
  const [cartMessage, setCartMessage] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchAvailability(variety.sku, quantity).then((result) => {
      if (cancelled) return;
      setAvailability(result.message);
      // bump the token so the highlight animation replays whenever the
      // stock number actually changes, not just on the first fetch
      setFetchToken((t) => t + 1);
    });
    return () => {
      cancelled = true;
    };
  }, [variety.sku, quantity]);

  const handleAddToCart = () => {
    addToCart(variety.sku, quantity).then(() => {
      setCartMessage(`${quantity} packet(s) of ${variety.name} added to your cart.`);
      setCartToken((t) => t + 1);
    });
  };

  return (
    <div className="seed-availability-panel">
      <h2>{variety.name}</h2>
      <p className="variety-description">{variety.description}</p>

      <label htmlFor="seed-quantity">Quantity</label>
      <input
        id="seed-quantity"
        type="number"
        min="1"
        max="20"
        value={quantity}
        aria-describedby="availability-status"
        onChange={(e) => setQuantity(Number(e.target.value))}
      />

      {availability && (
        <AvailabilityStatus key={fetchToken} message={availability} />
      )}

      <button className="add-to-cart" onClick={handleAddToCart}>
        Add to Cart
      </button>

      {cartMessage && (
        <AvailabilityStatus key={`cart-${cartToken}`} message={cartMessage} />
      )}
    </div>
  );
};

export default SeedAvailabilityPanel;
```

## CSS

```css
.seed-availability-panel {
  max-width: 420px;
  padding: 20px;
  border: 1px solid #d6ddd0;
  border-radius: 8px;
  font-family: sans-serif;
}

.variety-description {
  color: #445544;
  font-size: 14px;
  margin-bottom: 16px;
}

#seed-quantity {
  width: 70px;
  padding: 8px;
  border: 1px solid #a9b8a0;
  border-radius: 4px;
  font-size: 15px;
}

.availability-status {
  margin-top: 12px;
  padding: 8px 12px;
  background: #eef5e9;
  border-radius: 4px;
  font-size: 14px;
  color: #2f4a2f;
  animation: highlight-fade 900ms ease-out;
}

@keyframes highlight-fade {
  from {
    background: #d6ead0;
  }
  to {
    background: #eef5e9;
  }
}

.add-to-cart {
  display: block;
  margin-top: 14px;
  padding: 10px 18px;
  background: #3f6b3f;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  font-size: 15px;
  cursor: pointer;
}

.add-to-cart:focus-visible {
  outline: 3px solid #1f4d1f;
  outline-offset: 2px;
}
```

## Expected Behavior

- Changing the quantity re-checks availability for the selected seed variety and shows an updated status message (e.g., "12 packets in stock" or "Only 3 left — order soon").
- Adding to cart shows a confirmation message below the button.
- Both messages should be announced to screen reader users without requiring them to move focus.
- A highlight animation briefly fades in behind the status text whenever it changes, drawing sighted users' attention to the update.

## Accessibility Features Present

✓ Quantity input has a label associated via htmlFor
✓ Quantity input has aria-describedby pointing to the availability status region's id
✓ Availability and cart-confirmation messages render inside role="status" aria-live="polite" containers
✓ Add to Cart button has a visible focus indicator

## Accessibility Issues (Planted)

1. **MUST-FIND / CRITICAL: The status container is torn down and rebuilt on every update, so aria-live never observes a mutation.** `AvailabilityStatus` is rendered with `key={fetchToken}` (and separately `key={\`cart-${cartToken}\`}`), and both tokens are incremented on every successful fetch specifically to replay the CSS highlight-fade animation. Because the `key` changes, React unmounts the previous `role="status"` element and mounts an entirely new one — already containing the new message — rather than updating the text content of a persistent node. ARIA live regions only announce content that changes within an element already present in the accessibility tree; a freshly-inserted element that arrives with its content already in place is not an update to observe, so nothing is announced. This defeats both the availability status and the cart-confirmation message, despite `role="status"` and `aria-live="polite"` being present and technically correct in isolation.
   - Evidence: `seed-availability-panel.md` — `<AvailabilityStatus key={fetchToken} message={availability} />` and `<AvailabilityStatus key={\`cart-${cartToken}\`} message={cartMessage} />`; `fetchToken`/`cartToken` incremented on every update inside the `useEffect`/`handleAddToCart` callbacks
   - WCAG: 4.1.3 Status Messages
   - Impact: Screen reader users who change the quantity or add an item to the cart hear nothing — the same silent-update behavior the audit finding this PR cites was supposed to fix
   - User group: Screen reader users
   - Fix: Render a single, persistently-mounted status container (no changing `key`) and update only its text content on each fetch; if the fade animation needs to replay without remounting, retrigger it via a CSS class toggle or the Web Animations API instead of a key change

2. **SHOULD-FIND / MAJOR: The fetch-in-progress state has no announcement of its own, so the silence extends through the entire quantity-change interaction.** Between the user changing the quantity and the new availability fetch resolving, there is no `aria-busy`, no interim "Checking availability…" text, and no other signal exposed to assistive technology. Combined with Issue 1, a screen reader user who changes the quantity gets total silence from the moment they type until well after the (also-unannounced) result arrives.
   - Evidence: `seed-availability-panel.md` — the `useEffect` calls `fetchAvailability` with no loading-state text or `aria-busy` attribute anywhere in the render output
   - WCAG: 4.1.3 Status Messages
   - Impact: Compounds Issue 1 — there is no point in the interaction where a screen reader user learns anything changed
   - User group: Screen reader users
   - Fix: Set `aria-busy="true"` on the panel (or render brief "Checking availability…" text inside the persistent status container) while the fetch is pending

3. **SHOULD-FIND / MAJOR: The same broken remount pattern is reused for the cart-added confirmation, not just the availability message.** `handleAddToCart` calls the identical `AvailabilityStatus` component with a separately-incrementing `cartToken` as its `key`, so adding an item to the cart is silent for the same structural reason as Issue 1. This shows the defect is systemic to how the shared component is called, not a one-off mistake on a single message.
   - Evidence: `seed-availability-panel.md` — `<AvailabilityStatus key={\`cart-${cartToken}\`} message={cartMessage} />` inside `handleAddToCart`
   - WCAG: 4.1.3 Status Messages
   - Impact: A fix applied only to the availability message would leave the cart confirmation silently broken
   - User group: Screen reader users
   - Fix: Same fix as Issue 1, applied at both call sites — ideally by changing how `AvailabilityStatus` is mounted once, rather than patching each caller separately

## Difficulty Level

**HAS-BUGS** — `role="status"` and `aria-live="polite"` are present exactly where the audit finding said they were needed, and the quantity input's `aria-describedby` correctly references the status region's id. The defect is not a missing attribute — it is a remount mechanism that discards the live region on every update, a well-documented but easy-to-miss React anti-pattern (changing a `key` prop to force a fresh mount, usually added for an unrelated reason such as replaying a CSS animation).

## Frameworks & Environment

React 18+, standard CSS animations

## Notes

This fixture tests whether a reviewer can distinguish:

1. **Live region presence** (correctly done — `role="status"`, `aria-live="polite"` are both there) from **live region persistence** (broken — the container is a new DOM node on every update, so there is no stable element for AT to observe a mutation on). A reviewer who only checks for the presence of `aria-live`/`role="status"` attributes will mark this component clean.
2. The reason for the `key` change is legitimate-looking (replaying a highlight animation) and unrelated to accessibility on its face — tracing it to its effect on the live region requires understanding React's reconciliation model, not just reading ARIA attributes.
3. **False positive risk**: the quantity input's `aria-describedby="availability-status"` continues to work correctly even after the remount, because `aria-describedby` only requires a matching `id` to exist in the DOM at any given moment — it does not depend on the element being the *same* node over time the way a live-region announcement does. A reviewer who claims the `aria-describedby` association is "also broken by the remount" would be raising a false positive; only the live announcement is defeated, not the static description a user tabbing to the field would still hear on focus.

Expected verdict: REVISE. Expected baseline detection: low — the presence of `role="status"` and `aria-live="polite"` closely resembles a fixture that should score as clean, which is exactly what makes the remount mechanism easy to miss without tracing the `key` prop's effect on mount/unmount behavior.
