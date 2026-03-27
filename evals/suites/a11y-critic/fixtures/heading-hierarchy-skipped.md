# Fixture: Blog Post with Skipped Heading Levels

## Component Code

```jsx
const BlogPost = () => {
  return (
    <article className="blog-post">
      <h1>Introduction to Web Accessibility</h1>

      {/* BUG: Skips from h1 directly to h3 */}
      <h3>Why Accessibility Matters</h3>
      <p>
        Web accessibility ensures that everyone, including people with disabilities,
        can access and interact with web content effectively.
      </p>

      <h3>WCAG Guidelines</h3>
      <p>The Web Content Accessibility Guidelines (WCAG) provide a set of standards...</p>

      <h3>Common Issues</h3>
      <ul>
        <li>Missing alt text for images</li>
        <li>Poor color contrast</li>
        <li>Inaccessible forms</li>
      </ul>

      {/* BUG: Still h3, should be h2 for new section */}
      <h3>Getting Started</h3>

      {/* BUG: Then jumps to h2, inconsistent */}
      <h2>Tools and Resources</h2>
      <p>There are many tools available to help with accessibility testing...</p>

      <h2>Conclusion</h2>
      <p>Accessibility is not optional. It's a fundamental part of web development.</p>
    </article>
  );
};

export default BlogPost;
```

## CSS

```css
.blog-post {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  line-height: 1.6;
  color: #333;
}

.blog-post h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #0066cc;
}

.blog-post h2 {
  font-size: 24px;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #0066cc;
}

.blog-post h3 {
  font-size: 18px;
  margin-top: 20px;
  margin-bottom: 10px;
  color: #666;
}

.blog-post p {
  margin-bottom: 16px;
}

.blog-post ul {
  margin-left: 20px;
  margin-bottom: 16px;
}

.blog-post li {
  margin-bottom: 8px;
}
```

## Expected Behavior

- Blog post displays with clear heading hierarchy
- Sections are visually distinct
- Headings convey information hierarchy

## Accessibility Features Present

✓ Semantic heading elements
✓ No headings for visual styling only

## Accessibility Issues (Planted)

1. **MAJOR: Heading hierarchy skips levels (h1 → h3)** — Screen reader users relying on heading navigation (heading arrow keys) encounter unexpected jumps. Per WCAG 1.3.1, heading hierarchy should be logical and hierarchical.
   - Evidence: `heading-hierarchy-skipped.md:8-11` (h1 followed directly by h3, skipping h2)
   - WCAG citation: 1.3.1 Info and Relationships (document structure must be logical)
   - User group: Screen reader users navigating by headings
   - Expected: h1 should be followed by h2, not h3
   - Fix: Change first h3s to h2 (or add h2 as parent section)

2. **MAJOR: Inconsistent heading hierarchy (h3 then h2)** — After using h3 for subsections, suddenly switching to h2 breaks the logical structure. Screen reader users get confused about information hierarchy.
   - Evidence: `heading-hierarchy-skipped.md:20-21` (h3 followed later by h2, inconsistent)
   - WCAG citation: 1.3.1 Info and Relationships
   - User group: Screen reader users
   - Expected: Either all subsections are h2, or subsections under h2 are h3
   - Fix: Choose one hierarchy: either h1 > h2 > h3 or h1 > h3 (if h3 directly under h1)

## Difficulty Level

**HAS-BUGS** — Clear structural issue. Heading hierarchy is broken. This is a common mistake when content is added incrementally without reviewing the full structure.

## Frameworks & Environment

React, standard HTML/CSS

## Notes

Heading hierarchy is often checked visually (h1 is larger font) but not semantically (document structure). Screen reader users rely on proper h1 > h2 > h3 hierarchy. This fixture tests whether a11y-critic checks semantic structure, not just visual appearance.
