# Calibration Fixture C5: Drag-and-Drop Kanban Board

## Component Description

React kanban board with three columns (To Do, In Progress, Done) and draggable task cards. No keyboard alternative for drag-and-drop. Cards can be reordered within and moved between columns via mouse drag only.

## Component Code

```jsx
import React, { useState } from 'react';

const initialColumns = {
  todo: {
    title: 'To Do',
    cards: [
      { id: 'c1', title: 'Design homepage mockup', assignee: 'Alice', priority: 'High' },
      { id: 'c2', title: 'Write API documentation', assignee: 'Bob', priority: 'Medium' },
      { id: 'c3', title: 'Set up CI pipeline', assignee: 'Carol', priority: 'Low' },
    ],
  },
  progress: {
    title: 'In Progress',
    cards: [
      { id: 'c4', title: 'Implement auth flow', assignee: 'Alice', priority: 'High' },
      { id: 'c5', title: 'Database migration', assignee: 'Dave', priority: 'High' },
    ],
  },
  done: {
    title: 'Done',
    cards: [
      { id: 'c6', title: 'Project setup', assignee: 'Carol', priority: 'Low' },
    ],
  },
};

const KanbanBoard = () => {
  const [columns, setColumns] = useState(initialColumns);
  const [dragging, setDragging] = useState(null);
  const [dragOver, setDragOver] = useState(null);

  const handleDragStart = (cardId, fromCol) => {
    setDragging({ cardId, fromCol });
  };

  const handleDragOver = (e, colId) => {
    e.preventDefault();
    setDragOver(colId);
  };

  const handleDrop = (toCol) => {
    if (!dragging) return;
    const { cardId, fromCol } = dragging;
    if (fromCol === toCol) { setDragging(null); setDragOver(null); return; }

    setColumns(prev => {
      const next = JSON.parse(JSON.stringify(prev));
      const cardIdx = next[fromCol].cards.findIndex(c => c.id === cardId);
      const [card] = next[fromCol].cards.splice(cardIdx, 1);
      next[toCol].cards.push(card);
      return next;
    });
    setDragging(null);
    setDragOver(null);
  };

  return (
    <main className="kanban-page">
      <h1>Project Board</h1>
      <div className="kanban-board">
        {Object.entries(columns).map(([colId, col]) => (
          <section
            key={colId}
            className={`kanban-column ${dragOver === colId ? 'drag-over' : ''}`}
            onDragOver={(e) => handleDragOver(e, colId)}
            onDrop={() => handleDrop(colId)}
            aria-label={`${col.title} column — ${col.cards.length} cards`}
          >
            <h2>{col.title} <span className="card-count">({col.cards.length})</span></h2>
            {col.cards.map(card => (
              <div
                key={card.id}
                className="kanban-card"
                draggable
                onDragStart={() => handleDragStart(card.id, colId)}
                onDragEnd={() => { setDragging(null); setDragOver(null); }}
              >
                <h3>{card.title}</h3>
                <p className="card-meta">
                  <span className="assignee">{card.assignee}</span>
                  <span className={`priority priority-${card.priority.toLowerCase()}`}>{card.priority}</span>
                </p>
              </div>
            ))}
          </section>
        ))}
      </div>
    </main>
  );
};

export default KanbanBoard;
```

```css
.kanban-page { max-width: 1080px; margin: 0 auto; padding: 24px; font-family: system-ui; }
.kanban-page h1 { font-size: 1.75rem; margin-bottom: 20px; }

.kanban-board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }

.kanban-column {
  background: #f5f5f5; border-radius: 8px; padding: 16px; min-height: 300px;
  transition: background 0.2s;
}
.kanban-column.drag-over { background: #e3f2fd; }

.kanban-column h2 { font-size: 1rem; margin-bottom: 12px; color: #222; }
.card-count { color: #777; font-weight: 400; }

.kanban-card {
  background: #fff; border: 1px solid #ddd; border-radius: 6px;
  padding: 12px; margin-bottom: 8px; cursor: grab;
}
.kanban-card:active { cursor: grabbing; }
.kanban-card h3 { font-size: 0.95rem; margin: 0 0 8px; color: #111; }

.card-meta { display: flex; justify-content: space-between; font-size: 0.8rem; }
.assignee { color: #555; }
.priority { font-weight: 600; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; }
.priority-high { background: #ffebee; color: #c62828; }
.priority-medium { background: #fff8e1; color: #e65100; }
.priority-low { background: #e8f5e9; color: #2e7d32; }
```

## Why This Is a Calibration Fixture

This kanban board presents the **canonical keyboard accessibility failure** — drag-and-drop with no keyboard alternative — alongside cognitive complexity from spatial multi-column state tracking. It tests whether the escalation mechanism correctly flags Keyboard=HIGH and Cognitive=HIGH while keeping other perspectives appropriately low.

## Expected Alarm Levels

| Perspective | Expected | Rationale |
|---|---|---|
| Keyboard & Motor | **HIGH** | Drag-and-drop is mouse-only. Cards have `draggable` attribute but no onKeyDown handlers, no keyboard move mechanism. This is the primary accessibility barrier. |
| Cognitive & Neurodivergent | **HIGH** | Spatial organization requires tracking card positions across 3 columns. Mental model of "where things are" relies on visual spatial layout. Priority labels use color + text but column state is purely spatial. |
| Screen Reader & Semantic | **MEDIUM** | Columns have aria-labels with card counts, headings present. But drag-and-drop state changes (card moved from X to Y) have no announcements. Cards lack role descriptions. |
| Magnification & Reflow | **MEDIUM** | 3-column grid with fixed layout. At 200% zoom, columns may be too narrow; at 400%, likely need horizontal scroll. |
| Vestibular & Motion | **LOW** | Minimal animation — only the drag-over background transition (0.2s). No continuous or triggered motion. |
| Auditory Access | **LOW** | No audio content. |
| Environmental Contrast | **LOW** | Priority labels use both text AND background color. Column headers are labeled. No color-only information. |

## Frameworks

React 18+, HTML Drag and Drop API, CSS Grid
