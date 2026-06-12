import React from 'react';
import { useRouter, usePathname } from 'next/navigation';

const sections = [
  { id: 'overview', label: 'Overview', path: '/product/overview' },
  { id: 'specs', label: 'Specifications', path: '/product/specs' },
  { id: 'reviews', label: 'Reviews', path: '/product/reviews' },
  { id: 'support', label: 'Support', path: '/product/support' },
];

const ProductNavigation = () => {
  const router = useRouter();
  const pathname = usePathname();
  const activeIndex = sections.findIndex(s => pathname.startsWith(s.path));

  const handleKeyDown = (e, index) => {
    let newIndex;
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        newIndex = (index + 1) % sections.length;
        router.push(sections[newIndex].path);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        newIndex = (index - 1 + sections.length) % sections.length;
        router.push(sections[newIndex].path);
        break;
      case 'Home':
        e.preventDefault();
        router.push(sections[0].path);
        break;
      case 'End':
        e.preventDefault();
        router.push(sections[sections.length - 1].path);
        break;
      default:
        break;
    }
  };

  return (
    <div className="product-nav-container">
      <div role="tablist" aria-label="Product sections">
        {sections.map((section, index) => (
          <button
            key={section.id}
            role="tab"
            id={`tab-${section.id}`}
            aria-selected={index === activeIndex}
            aria-controls={`panel-${section.id}`}
            tabIndex={index === activeIndex ? 0 : -1}
            onClick={() => router.push(section.path)}
            onKeyDown={(e) => handleKeyDown(e, index)}
            className={`product-nav-tab ${index === activeIndex ? 'active' : ''}`}
          >
            {section.label}
          </button>
        ))}
      </div>

      <div
        role="tabpanel"
        id={`panel-${sections[activeIndex >= 0 ? activeIndex : 0].id}`}
        aria-labelledby={`tab-${sections[activeIndex >= 0 ? activeIndex : 0].id}`}
        tabIndex={0}
        className="product-content"
      >
        {/* Page content rendered by Next.js router */}
      </div>
    </div>
  );
};

export default ProductNavigation;
