import React, { useState, useEffect } from 'react';

const products = [
  { id: 1, name: 'Wireless Headphones', price: '$149', badge: 'NEW', image: '/img/headphones.jpg' },
  { id: 2, name: 'Mechanical Keyboard', price: '$89', badge: 'SALE', image: '/img/keyboard.jpg' },
  { id: 3, name: 'USB-C Hub', price: '$49', badge: 'HOT', image: '/img/hub.jpg' },
  { id: 4, name: 'Webcam Pro', price: '$129', badge: 'NEW', image: '/img/webcam.jpg' },
];

const ProductCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % products.length);
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  const goToPrev = () => {
    setCurrentIndex((prev) => (prev - 1 + products.length) % products.length);
  };

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % products.length);
  };

  const product = products[currentIndex];

  return (
    <div className="carousel-wrapper" data-parallax="true">
      <div
        className="carousel-track"
        style={{
          transform: `translateX(-${currentIndex * 100}%)`,
          transition: 'transform 0.6s ease',
        }}
      >
        {products.map((p) => (
          <div key={p.id} className="carousel-slide">
            <img src={p.image} alt={p.name} />
            <span className="product-badge">{p.badge}</span>
            <h2>{p.name}</h2>
            <p className="price">{p.price}</p>
          </div>
        ))}
      </div>

      {/* Keyboard navigation works correctly — prev/next buttons are focusable and labeled */}
      <button
        className="carousel-btn carousel-prev"
        onClick={goToPrev}
        aria-label="Previous product"
      >
        ‹
      </button>
      <button
        className="carousel-btn carousel-next"
        onClick={goToNext}
        aria-label="Next product"
      >
        ›
      </button>

      <div className="carousel-dots">
        {products.map((_, i) => (
          <span
            key={i}
            className={`dot ${i === currentIndex ? 'active' : ''}`}
            aria-hidden="true"
          />
        ))}
      </div>
    </div>
  );
};

export default ProductCarousel;
