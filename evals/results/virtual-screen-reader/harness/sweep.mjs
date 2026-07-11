// Phase 2 cross-validation sweep: @guidepup/virtual-screen-reader 0.32.1 vs the
// announcement-class a11y-critic fixtures (docs/virtual-screen-reader-adoption-assessment.md).
//
// Each fixture's React component is replicated at the DOM layer — the layer VSR sees.
// Directions per defect fixture: "buggy" (planted defect; expect silence = defect evidence)
// and "fixed" (rubric's corrected pattern, written robustly; expect announcement).
// The clean fixture is the false-alarm trap (expect announcements, no false-silent).
// The adversarial fixture is a measurement demo (record what fires; no verdict).
//
// Run:  npm install && node sweep.mjs        (writes ../raw/<fixture>.json)
import { JSDOM } from "jsdom";
import { writeFileSync, mkdirSync } from "node:fs";

const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
  pretendToBeVisual: true,
  url: "https://fixture.local/",
});
globalThis.window = dom.window;
globalThis.document = dom.window.document;
for (const k of ["Node", "Element", "HTMLElement", "MutationObserver", "getComputedStyle"]) {
  globalThis[k] = dom.window[k];
}

const { virtual } = await import("@guidepup/virtual-screen-reader");

const settle = () => new Promise((r) => setTimeout(r, 50));

/** Start VSR on a fresh body, run `action`, return only the phrases it caused. */
async function capture(setupHtml, action) {
  document.body.innerHTML = setupHtml;
  await virtual.start({ container: document.body });
  await settle();
  const before = (await virtual.spokenPhraseLog()).length;
  await action();
  await settle();
  const log = await virtual.spokenPhraseLog();
  await virtual.stop();
  document.body.innerHTML = "";
  return log.slice(before);
}

/** Bounded full walk (calibration rule 1: never while-true). */
async function walk(setupHtml, maxSteps = 60) {
  document.body.innerHTML = setupHtml;
  await virtual.start({ container: document.body });
  const phrases = [];
  for (let i = 0; i < maxSteps; i++) {
    await virtual.next();
    const p = await virtual.lastSpokenPhrase();
    phrases.push(p);
    if (p === "end of document") break;
  }
  await virtual.stop();
  document.body.innerHTML = "";
  return phrases;
}

const results = {};

// ───────────────────────── toast-notification-no-role ─────────────────────────
{
  const page = `<main><h1>Orders</h1><button>Save order</button></main>`;
  results["toast-notification-no-role"] = {
    buggy_mount_with_content_no_role: await capture(page, () => {
      const t = document.createElement("div");
      t.className = "toast-notification";
      t.textContent = "Item saved";
      document.body.appendChild(t);
    }),
    naive_fix_mount_with_content_role_alert: await capture(page, () => {
      const t = document.createElement("div");
      t.setAttribute("role", "alert");
      t.textContent = "Item saved";
      document.body.appendChild(t);
    }),
    robust_fix_persistent_container: await capture(
      page + `<div role="status" id="toast-region"></div>`,
      () => { document.getElementById("toast-region").textContent = "Item saved"; }
    ),
  };
}

// ─────────────────────── infinite-scroll-no-announcement ───────────────────────
{
  const listPage = `<div class="infinite-scroll-container"><ul id="items">
    <li>Item 1</li><li>Item 2</li></ul><div class="scroll-trigger"></div></div>`;
  const appendItems = () => {
    for (let i = 3; i <= 5; i++) {
      const li = document.createElement("li");
      li.textContent = `Item ${i}`;
      document.getElementById("items").appendChild(li);
    }
  };
  results["infinite-scroll-no-announcement"] = {
    buggy_items_load_silently: await capture(listPage, appendItems),
    fixed_persistent_status_region: await capture(
      listPage + `<div role="status" id="load-status"></div>`,
      () => {
        appendItems();
        document.getElementById("load-status").textContent = "3 more items loaded";
      }
    ),
    // MF3 (no main landmark) is structural: the walk shows no landmark phrases.
    buggy_walk_no_landmark_phrases: await walk(listPage),
  };
}

// ───────────────────────── image-carousel-no-region ─────────────────────────
{
  const carousel = (live) => `<div class="carousel">
    <div class="carousel-images"><img id="img" src="a.jpg" alt="Carousel image 1"></div>
    <button aria-label="Previous image">Previous</button>
    <button aria-label="Next image">Next</button>
    <div class="carousel-indicators">
      <button aria-label="Go to image 1" class="active">1</button>
      <button aria-label="Go to image 2">2</button>
    </div>${live ? `<div aria-live="polite" id="carousel-status"></div>` : ""}</div>`;
  const nextImage = () => {
    const img = document.getElementById("img");
    img.setAttribute("src", "b.jpg");
    img.setAttribute("alt", "Carousel image 2");
  };
  results["image-carousel-no-region"] = {
    buggy_image_change_silent: await capture(carousel(false), nextImage),
    fixed_persistent_polite_region: await capture(carousel(true), () => {
      nextImage();
      document.getElementById("carousel-status").textContent = "Image 2 of 2";
    }),
    // MF1/MF2/MF4 are structural: walk shows no region boundary and no aria-current state.
    buggy_walk_structure: await walk(carousel(false)),
  };
}

// ───────────────────────── async-form-vague-success ─────────────────────────
{
  // Live region infrastructure is CORRECT in this fixture (FLAWED-class): persistent,
  // role=status, aria-live=polite, aria-atomic. The must-find is announcement QUALITY.
  const page = `<div><h2>Send Us Feedback</h2>
    <div role="status" aria-live="polite" aria-atomic="true" id="form-status"></div>
    <form><button type="submit">Send Feedback</button></form></div>`;
  const region = () => document.getElementById("form-status");
  results["async-form-vague-success"] = {
    as_written_submit_lifecycle: await capture(page, async () => {
      region().innerHTML = `<p>Submitting your feedback...</p>`;
      await settle();
      region().innerHTML = ``;               // the 'clearing' intermediate state
      await settle();
      region().innerHTML = `<p>Your submission was successful!</p>`;
    }),
    fixed_contextual_message: await capture(page, () => {
      region().innerHTML = `<p>Your feedback has been sent. We'll respond to you@example.com within 2 business days.</p>`;
    }),
    // SHOULD-FIND aria-busy timing gap: OUT OF SCOPE — aria-busy unsupported (upstream #36).
    aria_busy_timing: "OUT_OF_SCOPE_upstream_issue_36",
  };
}

// ──────────────────────── multistep-form-error-clearing ────────────────────────
{
  const page = `<form class="wizard-form">
    <div aria-live="polite" class="error-region" id="errors"></div>
    <label for="email">Email Address</label><input id="email" type="email">
    <button type="button">Next</button></form>`;
  results["multistep-form-error-clearing"] = {
    errors_appear_announced: await capture(page, () => {
      document.getElementById("errors").innerHTML =
        `<ul class="error-list"><li>Enter a valid email address.</li></ul>`;
    }),
    buggy_error_clearance_silent: await capture(page, async () => {
      document.getElementById("errors").innerHTML =
        `<ul class="error-list"><li>Enter a valid email address.</li></ul>`;
      await settle();
      const before = (await virtual.spokenPhraseLog()).length;
      document.getElementById("errors").innerHTML = ``;   // user fixed the field
      await settle();
      // stash the slice for THIS mutation only
      results.__clearance_slice = (await virtual.spokenPhraseLog()).slice(before);
    }),
    fixed_clearance_confirmation: await capture(page, async () => {
      document.getElementById("errors").innerHTML =
        `<ul class="error-list"><li>Enter a valid email address.</li></ul>`;
      await settle();
      document.getElementById("errors").innerHTML = `<p>Email error resolved.</p>`;
    }),
  };
  results["multistep-form-error-clearing"].buggy_error_clearance_silent =
    results.__clearance_slice;
  delete results.__clearance_slice;
}

// ─────────────────────── form-field-vs-summary-errors (ADVERSARIAL) ───────────────────────
{
  // Both patterns individually correct; question is the on-submit interaction effect.
  // Measurement demo: record exactly what fires when summary (role=alert, mounted with
  // content) and 4 inline errors (inserted into persistent aria-live wrappers) land at once.
  const fields = ["email", "password", "confirmPassword", "displayName"];
  const page = `<form class="reg-form"><h1>Create your account</h1><div id="summary-slot"></div>
    ${fields.map((f) => `<div class="form-group"><label for="field-${f}">${f}</label>
      <input id="field-${f}"><div aria-live="polite" id="inline-${f}"></div></div>`).join("")}
    <button type="submit">Create account</button></form>`;
  const messages = {
    email: "Email address is required.",
    password: "Password is required.",
    confirmPassword: "Please confirm your password.",
    displayName: "Display name is required.",
  };
  results["form-field-vs-summary-errors"] = {
    adversarial_submit_measurement: await capture(page, () => {
      document.getElementById("summary-slot").innerHTML =
        `<div role="alert" tabindex="-1"><h2>There are 4 errors in this form</h2><ul>` +
        fields.map((f) => `<li><a href="#field-${f}">${messages[f]}</a></li>`).join("") +
        `</ul></div>`;
      for (const f of fields) {
        document.getElementById(`inline-${f}`).innerHTML =
          `<span class="error-text">${messages[f]}</span>`;
      }
    }),
    note: "ADVERSARIAL fixture — no verdict; phrase log is evidence input to the tradeoff judgment.",
  };
}

// ─────────────────────── search-results-dynamic-clean (CLEAN trap) ───────────────────────
{
  const page = `<div class="search-container">
    <form><label for="q">Search</label><input id="q" type="text" aria-label="Search query">
    <button type="submit">Search</button></form>
    <div role="status" aria-live="polite" aria-atomic="true" id="search-status"></div>
    <div id="results"></div></div>`;
  const region = () => document.getElementById("search-status");
  results["search-results-dynamic-clean"] = {
    clean_searching_announced: await capture(page, () => {
      region().textContent = "Searching...";
    }),
    clean_results_count_announced: await capture(page, async () => {
      region().textContent = "Searching...";
      await settle();
      region().textContent = "Found 3 results";
      document.getElementById("results").innerHTML =
        `<h2>Search Results</h2><ul><li><h3>Result 1</h3></li><li><h3>Result 2</h3></li><li><h3>Result 3</h3></li></ul>`;
    }),
  };
}

mkdirSync(new URL("../raw/", import.meta.url), { recursive: true });
for (const [fixture, data] of Object.entries(results)) {
  writeFileSync(
    new URL(`../raw/${fixture}.json`, import.meta.url),
    JSON.stringify({ tool: "@guidepup/virtual-screen-reader@0.32.1", env: "node+jsdom", date: "2026-07-11", fixture, ...data }, null, 2)
  );
}
console.log(JSON.stringify(results, null, 2));
