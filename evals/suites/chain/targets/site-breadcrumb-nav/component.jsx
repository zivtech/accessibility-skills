import React from 'react';

const Breadcrumbs = ({ trail }) => (
  <nav aria-label="Breadcrumb" className="breadcrumbs">
    <ol>
      {trail.map((crumb, i) => {
        const isCurrent = i === trail.length - 1;
        return (
          <li key={crumb.href}>
            {isCurrent ? (
              <span aria-current="page">{crumb.label}</span>
            ) : (
              <a href={crumb.href}>{crumb.label}</a>
            )}
          </li>
        );
      })}
    </ol>
  </nav>
);

export default Breadcrumbs;
