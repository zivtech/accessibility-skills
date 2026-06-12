import React, { useState, useRef, useEffect } from 'react';

const SubscribeModal = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [submitted, setSubmitted] = useState(false);


  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="modal-backdrop">
        <div className="modal-container">
          <p className="modal-success">Thanks, {name}! You're subscribed.</p>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-backdrop">
      <div className="modal-container">

        <div className="modal-header">
          {/* id present for potential aria-labelledby — but dialog never references it */}
          <h2 id="modal-title" className="modal-title">Subscribe to Updates</h2>
          <button
            className="modal-close"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form" noValidate>

          {/* Works: label correctly associated with input via htmlFor/id */}
          <div className="form-group">
            <label htmlFor="modal-name">Your name</label>
            <input
              id="modal-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              aria-required="true"
            />
          </div>

          {/* Works: label correctly associated with input via htmlFor/id */}
          <div className="form-group">
            <label htmlFor="modal-email">Email address</label>
            <input
              id="modal-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              aria-required="true"
            />
          </div>

          {/* Works: real <button> elements, keyboard-activatable */}
          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Subscribe
            </button>
          </div>

        </form>
      </div>
    </div>
  );
};

const SubscribePage = () => {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);

  // triggerRef exists but is never used to restore focus on close.
  const handleClose = () => {
    setIsOpen(false);
    // Missing: triggerRef.current?.focus();
  };

  return (
    <main className="page-main">
      <h1>Newsletter</h1>
      <p>Stay informed about our latest updates and announcements.</p>

      <button
        ref={triggerRef}
        className="btn-open"
        onClick={() => setIsOpen(true)}
        aria-haspopup="dialog"
      >
        Subscribe Now
      </button>

      {/* Background content remains fully interactive while modal is open */}
      <nav className="background-nav">
        <a href="/home">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
      </nav>

      {isOpen && <SubscribeModal onClose={handleClose} />}
    </main>
  );
};

export default SubscribePage;
