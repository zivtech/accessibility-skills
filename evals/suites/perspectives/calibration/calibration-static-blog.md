# Calibration Fixture C1: Static Blog Post

## Component Code

```jsx
import React from 'react';

const BlogPost = ({ title, author, date, content, heroImage }) => {
  return (
    <article className="blog-post">
      <header>
        <h1>{title}</h1>
        <p className="byline">
          By <span className="author">{author}</span> |{' '}
          <time dateTime={date}>{new Date(date).toLocaleDateString()}</time>
        </p>
      </header>

      <figure className="hero">
        <img src={heroImage.src} alt={heroImage.alt} />
        <figcaption>{heroImage.caption}</figcaption>
      </figure>

      <div className="content" dangerouslySetInnerHTML={{ __html: content }} />

      <footer className="post-footer">
        <h2>About the Author</h2>
        <p>{author} writes about web development and accessibility.</p>
      </footer>
    </article>
  );
};

export default BlogPost;
```

```css
.blog-post {
  max-width: 720px;
  margin: 0 auto;
  padding: 1rem;
  font-size: 1rem;
  line-height: 1.6;
  color: #1a1a1a;
  background: #ffffff;
}

.hero img {
  width: 100%;
  height: auto;
}

.byline {
  color: #555555;
  font-size: 0.9rem;
}

.content h2 { margin-top: 2rem; }
.content p { margin-bottom: 1rem; }
```

## Component Description

A standard blog post page with a title, author byline, hero image with alt text and figcaption, body content (rendered from CMS HTML), and an author bio footer. Pure text and image content — no video, no audio, no animation, no interactive widgets beyond default link behavior.

## Why This Is a Calibration Fixture

This is the simplest archetype — static content with minimal interactivity. Most perspectives should be LOW because the component has no video (auditory), no animation (vestibular), no complex interactions (keyboard beyond links), and a clean single-column layout (magnification). Screen Reader and Cognitive warrant MEDIUM because any text content should have good semantic structure and readable prose.

## Expected Alarm Levels

| Perspective | Expected Level | Rationale |
|---|---|---|
| Magnification & Reflow | LOW | Single column, responsive, no fixed layout |
| Environmental Contrast | LOW | High contrast text (#1a1a1a on #fff), no color-coded information |
| Vestibular & Motion | LOW | No animation, no auto-playing content |
| Auditory Access | LOW | No audio or video content |
| Keyboard & Motor | LOW | No custom interactive widgets, only native links |
| Screen Reader & Semantic | MEDIUM | Article semantics, heading hierarchy, image alt text need verification |
| Cognitive & Neurodivergent | MEDIUM | Reading level, content structure, paragraph length need verification |
