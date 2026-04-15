import React from 'react';
import { Clock, Archive } from 'lucide-react';

export default function PromptHistoryPanel({ promptHistory, onLoadVersion, onSaveVersion, currentPrompt }) {
  if (!promptHistory) return null;

  return (
    <div className="glass rounded-[var(--radius)] p-6 border border-slate-700 shadow-2xl mt-8">
      <div className="flex items-center justify-between mb-6 gap-3">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Prompt History</h2>
          <p className="text-sm text-zinc-400">Track versions and store prompt history for regression analysis.</p>
        </div>
        <button
          onClick={() => onSaveVersion(currentPrompt, `v${promptHistory.length + 1}`)}
          className="inline-flex items-center gap-2 rounded-full bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-500 transition"
        >
          <Archive size={16} />
          Save Version
        </button>
      </div>

      {promptHistory.length === 0 ? (
        <div className="text-zinc-400">No prompt history found for the current prompt.</div>
      ) : (
        <div className="space-y-3">
          {promptHistory.map((entry, index) => (
            <div key={index} className="bg-zinc-950/70 border border-zinc-800 rounded-3xl p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <div className="text-sm text-zinc-500 mb-1 flex items-center gap-2">
                    <Clock size={14} />
                    <span>{new Date(entry.created_at).toLocaleString()}</span>
                  </div>
                  <div className="text-white font-semibold">{entry.version || `v${index + 1}`}</div>
                </div>
                <button
                  onClick={() => onLoadVersion(entry.prompt)}
                  className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-white hover:bg-white/15 transition"
                >
                  Load
                </button>
              </div>
              <p className="text-zinc-300 text-sm mt-3 whitespace-pre-wrap">{entry.prompt}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
