# Fixture: Chat Interface With Cognitive Load Issues

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

// CSS
/*
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 680px;
  margin: 0 auto;
  font-family: system-ui, sans-serif;
  background: #fff;
  border: 1px solid #e0e0e0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  /* NOT a bug — aria-live=polite is correct for chat messages */
}

.message-bubble {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
}

.message-bubble.user {
  background: #2b6cb0;
  color: #fff;
  align-self: flex-end;
}

.message-bubble.assistant {
  background: #f0f0f0;
  color: #111;
  align-self: flex-start;
}

.message-timestamp {
  font-size: 11px;
  color: #999;
  /* BUG: Relative timestamps ("2 minutes ago") update every 60s while the user is
     reading — content changes without user interaction, disorienting for cognitive users */
  transition: none;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 10px 14px;
  background: #f0f0f0;
  border-radius: 16px;
  align-self: flex-start;
  width: fit-content;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
  /* BUG: Infinite bounce animation with no prefers-reduced-motion override */
  animation: bounce 0.6s infinite alternate;
}

@keyframes bounce {
  from { transform: translateY(0); }
  to   { transform: translateY(-6px); }
}

/* BUG: No @media (prefers-reduced-motion: reduce) rule to suppress typing animation */

.new-message-flash {
  /* BUG: New message notification relies on a background-color flash animation only —
     no text "New message" label, no sound option, no aria-live for the notification bar */
  animation: flashBg 0.4s ease-out;
  background: #ebf8ff;
}

@keyframes flashBg {
  0%   { background-color: #bee3f8; }
  100% { background-color: transparent; }
}

.chat-input-row {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
}

.chat-input {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  resize: none;
  /* NOT a bug — textarea has aria-label */
}

.btn-send {
  background: #2b6cb0;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 20px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 600;
  /* NOT a bug — send button is keyboard accessible with correct aria-label */
}

.btn-send:focus-visible {
  outline: 2px solid #2b6cb0;
  outline-offset: 2px;
}

.emoji-picker-btn {
  background: none;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  font-size: 18px;
  /* NOT a bug — emoji picker toggle button has aria-label */
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
  padding: 8px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  position: absolute;
  bottom: 70px;
  /* BUG: Emoji buttons have no keyboard grid navigation — Tab moves through all 64 buttons
     linearly; no arrow-key grid navigation, no focus trap, no Escape to close */
}

.emoji-btn {
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.emoji-btn:hover {
  background: #f0f0f0;
}

/* BUG: .emoji-btn has no :focus-visible styles — keyboard focus not visible in grid */
*/

const INITIAL_MESSAGES = [
  { id: 1, role: 'assistant', text: 'Hello! How can I help you today?', time: new Date(Date.now() - 180000) },
  { id: 2, role: 'user', text: 'I need help with my order.', time: new Date(Date.now() - 120000) },
  { id: 3, role: 'assistant', text: 'Sure! Can you share your order number?', time: new Date(Date.now() - 60000) },
];

const EMOJI_LIST = ['😀','😂','😍','🤔','👍','👎','❤️','🎉','🔥','✅','❌','⚠️',
  '😊','😅','🥺','😎','🙏','💯','🚀','💡','📌','🗓️','📊','💬',
  '😴','🤣','😢','😤','🤯','🎯','🏆','💪','🌟','🎨','📝','🔑',
  '😋','🤗','😇','😑','🦾','🧠','💎','🌈','⚡','🎵','📣','🔔',
  '🌍','🏠','🚗','✈️','🍕','☕','🎮','📱','💻','🔒','📧','🗺️'];

const formatRelativeTime = (date) => {
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'just now';
  if (diffMin === 1) return '1 minute ago';
  return `${diffMin} minutes ago`;
};

const ChatInterface = () => {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [, setTick] = useState(0);
  const messagesEndRef = useRef(null);

  // BUG: Auto-scroll fires on every message update with no pause mechanism.
  // WCAG 2.2.2 (Pause, Stop, Hide) — user has no way to pause auto-scroll while reading.
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // BUG: Relative timestamps update every 60s via setInterval.
  // Content changes while user reads — no way to freeze timestamps.
  useEffect(() => {
    const id = setInterval(() => setTick((n) => n + 1), 60000);
    return () => clearInterval(id);
  }, []);

  const sendMessage = () => {
    if (!inputValue.trim()) return;
    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: inputValue,
      time: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue('');
    setIsTyping(true);

    // Simulate assistant reply after 1.5s
    setTimeout(() => {
      setIsTyping(false);
      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        // BUG: New message added to messages triggers auto-scroll AND a color flash
        // New message notification is color-flash only — no text announcement beyond aria-live
        text: 'Thanks for your message. Let me look into that for you.',
        time: new Date(),
        isNew: true,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    }, 1500);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const insertEmoji = (emoji) => {
    setInputValue((prev) => prev + emoji);
    setShowEmojiPicker(false);
  };

  return (
    <div className="chat-container">
      {/* aria-live=polite is correct here — NOT a bug */}
      <div
        className="chat-messages"
        aria-live="polite"
        aria-label="Conversation"
        role="log"
      >
        {messages.map((msg) => (
          <div key={msg.id}>
            <div
              className={`message-bubble ${msg.role} ${msg.isNew ? 'new-message-flash' : ''}`}
            >
              {/* BUG: new-message-flash class applies color animation only —
                  the visual-flash notification has no text label or aria-live for the
                  "new message" notification specifically (role=log handles content,
                  but the flash as a distinct "new" signal is color-only) */}
              {msg.text}
            </div>
            <div className="message-timestamp">
              {/* BUG: Relative timestamp updates every 60s without user action */}
              {formatRelativeTime(msg.time)}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="typing-indicator" aria-label="Assistant is typing">
            {/* BUG: Infinite bounce animation with no prefers-reduced-motion override */}
            <span className="typing-dot" />
            <span className="typing-dot" style={{ animationDelay: '0.2s' }} />
            <span className="typing-dot" style={{ animationDelay: '0.4s' }} />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-row">
        {/* NOT a bug — emoji picker toggle has aria-label and aria-expanded */}
        <button
          className="emoji-picker-btn"
          aria-label="Open emoji picker"
          aria-expanded={showEmojiPicker}
          onClick={() => setShowEmojiPicker((v) => !v)}
        >
          😊
        </button>

        {showEmojiPicker && (
          <div className="emoji-grid" role="grid" aria-label="Emoji picker">
            {/* BUG: No arrow-key grid navigation — tabbing through 64 emoji one by one */}
            {/* BUG: No Escape key handler to close the picker */}
            {/* BUG: Emoji buttons have no :focus-visible styles */}
            {EMOJI_LIST.map((emoji) => (
              <button
                key={emoji}
                className="emoji-btn"
                onClick={() => insertEmoji(emoji)}
                aria-label={emoji}
                // BUG: No onKeyDown handler for arrow navigation within grid
              >
                {emoji}
              </button>
            ))}
          </div>
        )}

        {/* NOT a bug — textarea is labeled and keyboard operable */}
        <textarea
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="Type a message"
          rows={1}
          placeholder="Type a message..."
        />

        {/* NOT a bug — send button is keyboard accessible */}
        <button
          className="btn-send"
          onClick={sendMessage}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
```

## Expected Behavior

- Chat interface where auto-scroll can be paused while reading (e.g., scroll-lock when user scrolls up)
- Typing indicator animation respects `prefers-reduced-motion` (stops or fades when reduced-motion is set)
- New message notification uses a visible "New message" text label or badge in addition to any color change
- Timestamps are stable while reading — relative time either freezes or only updates on focus-out
- Emoji picker supports arrow-key grid navigation, Escape to close, and visible focus styles on each emoji button
- Send button, textarea, and emoji picker toggle are all keyboard-accessible

## Accessibility Features Present

- Chat message area uses `role="log"` and `aria-live="polite"` — correct pattern for chat
- Emoji picker toggle button has `aria-label` and `aria-expanded`
- Message textarea has `aria-label="Type a message"`
- Send button has `aria-label="Send message"`
- Typing indicator has `aria-label="Assistant is typing"`
- Send on Enter (without Shift) is a standard chat convention — not a keyboard trap

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Auto-scroll with no pause mechanism** — Every time a new message is added, `scrollIntoView({ behavior: 'smooth' })` fires unconditionally. Users who have scrolled up to re-read earlier messages are forcibly scrolled down. WCAG 2.2.2 (Pause, Stop, Hide) requires that automatically moving content can be paused or stopped by the user.
   - Evidence: `chat-cognitive-load.md` — `useEffect` calling `messagesEndRef.current?.scrollIntoView` on every `messages` state change; no scroll-lock mechanism
   - User group: Users with cognitive disabilities; users with attention difficulties; all users reading earlier messages
   - Expected fix: Track whether the user has manually scrolled up; suppress auto-scroll when scroll position is not at the bottom

2. **MAJOR: Typing indicator animation has no `prefers-reduced-motion` override** — The `.typing-dot` elements use an infinite `bounce` CSS animation with no `@media (prefers-reduced-motion: reduce)` rule. Users with vestibular disorders who have set the OS-level reduced-motion preference will still see the continuous bouncing animation.
   - Evidence: `.typing-dot { animation: bounce 0.6s infinite alternate }` with no corresponding reduced-motion media query in the CSS block; `/* BUG: No @media (prefers-reduced-motion: reduce) */` comment
   - User group: Users with vestibular disorders; users with photosensitive epilepsy; users who have enabled reduced-motion
   - Expected fix: Add `@media (prefers-reduced-motion: reduce) { .typing-dot { animation: none; } }` and substitute a non-animated indicator (e.g., "..." text)

3. **MAJOR: New message notification is color-flash only, no text or sound option** — The `new-message-flash` CSS class applies a `flashBg` animation that transitions the bubble background from blue to transparent. This color flash is the only "new message" signal beyond the `aria-live` content announcement. Users who have disabled animations, have color vision deficiencies, or are in high-contrast mode receive no distinct "new" signal.
   - Evidence: `.new-message-flash { animation: flashBg 0.4s ease-out }` — color-only; no "New" text badge, no non-animated visual indicator, no sound-option control
   - User group: Users with vestibular disorders (animation); users with color vision deficiencies; users in high-contrast mode
   - Expected fix: Add a visible "New" text badge or non-animated outline on new messages; ensure the visual indicator persists beyond the animation duration

4. **MINOR: Relative timestamps update every 60 seconds without user action** — The `setInterval` in the second `useEffect` calls `setTick` every 60 seconds, causing all timestamps to re-render. Content changes while the user reads, which can be disorienting for users with cognitive or attention disabilities.
   - Evidence: `useEffect` with `setInterval(..., 60000)` calling `setTick` — triggers component re-render and timestamp recalculation every minute
   - User group: Users with cognitive disabilities; users with attention difficulties
   - Expected fix: Freeze timestamps until the user sends a new message or refocuses the window; or use absolute timestamps (e.g., "2:34 PM") that do not change

5. **MINOR: Emoji picker has no keyboard grid navigation and no visible focus styles** — The emoji grid renders 64 `<button>` elements with no arrow-key navigation, no Escape handler to close the picker, and no `:focus-visible` CSS on the individual emoji buttons. Keyboard users must Tab through all 64 items sequentially.
   - Evidence: `.emoji-btn` has no `:focus-visible` styles in CSS block; `/* BUG: No arrow-key grid navigation */` comment in emoji grid render; no `onKeyDown` handler on emoji buttons
   - User group: Keyboard-only users; motor-impaired users using switch access
   - Expected fix: Implement `role="gridcell"` on each emoji button with arrow-key navigation (`useRef` + focus management); add `onKeyDown` Escape handler on the grid container; add `:focus-visible` outline to `.emoji-btn`

## Difficulty Level

**HAS-BUGS** — New dimensions: cognitive overload (auto-scroll, timestamp churn) and vestibular/motion (typing animation, new-message flash). The send button, textarea, and emoji picker toggle are all correctly implemented and are intentional true negatives. The `aria-live="polite"` on the chat log is correct — the bug is specifically the color-flash-only "new" signal layered on top of it.

## Frameworks

React 18+, CSS animations, `prefers-reduced-motion` (expected but absent), `IntersectionObserver` or scroll event (expected but absent)
