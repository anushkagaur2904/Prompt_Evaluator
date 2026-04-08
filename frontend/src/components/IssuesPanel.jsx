import React from 'react';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

export default function IssuesPanel({ issues }) {
  if (!issues || issues.length === 0) {
    return (
      <div className="glass rounded-[var(--radius)] p-6">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <CheckCircle2 className="text-emerald-500" />
          No Issues Found
        </h2>
        <p className="text-zinc-400">This prompt is very well-structured!</p>
      </div>
    );
  }

  return (
    <div className="glass rounded-[var(--radius)] p-6 border-l-4 border-l-red-500/50">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <AlertCircle className="text-red-400" />
        Identified Issues
      </h2>
      <ul className="space-y-3">
        {issues.map((issue, idx) => (
          <li key={idx} className="flex items-start gap-3 bg-red-500/5 p-3 rounded-md border border-red-500/10">
            <span className="text-zinc-300 text-sm leading-relaxed">{issue}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
