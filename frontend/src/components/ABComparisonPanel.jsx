import React from 'react';

export default function ABComparisonPanel({ abResult }) {
  if (!abResult) return null;

  return (
    <div className="glass rounded-[var(--radius)] p-6 border border-violet-500/20 shadow-2xl mt-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold gradient-text">A/B Prompt Comparison</h2>
          <p className="text-sm text-zinc-400 mt-1">Compare two prompt variants and view deterministic evaluation scores.</p>
        </div>
        <span className={`px-4 py-2 rounded-full text-xs font-semibold ${abResult.regression_detected ? 'bg-red-500/15 text-red-300 border border-red-500/20' : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/20'}`}>
          {abResult.regression_detected ? 'Regression Detected' : 'No Regression'}
        </span>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="bg-zinc-900/90 rounded-3xl p-5 border border-zinc-800">
          <h3 className="text-lg font-semibold text-white mb-3">Prompt A</h3>
          <div className="text-zinc-300 text-sm whitespace-pre-wrap p-4 bg-zinc-950/40 rounded-xl border border-zinc-800 mb-4">
            {abResult.prompt_a}
          </div>
          <div className="space-y-3">
            <div className="text-sm text-zinc-400">Score: <span className="text-white font-semibold">{abResult.score_a}/10</span></div>
            <div className="text-sm text-zinc-400">Issues:</div>
            <ul className="list-disc list-inside text-zinc-300 text-sm space-y-1">
              {abResult.issues_a.length > 0 ? abResult.issues_a.map((issue, idx) => (
                <li key={idx}>{issue}</li>
              )) : <li>No issues detected.</li>}
            </ul>
          </div>
        </div>

        <div className="bg-zinc-900/90 rounded-3xl p-5 border border-zinc-800">
          <h3 className="text-lg font-semibold text-white mb-3">Prompt B</h3>
          <div className="text-zinc-300 text-sm whitespace-pre-wrap p-4 bg-zinc-950/40 rounded-xl border border-zinc-800 mb-4">
            {abResult.prompt_b}
          </div>
          <div className="space-y-3">
            <div className="text-sm text-zinc-400">Score: <span className="text-white font-semibold">{abResult.score_b}/10</span></div>
            <div className="text-sm text-zinc-400">Issues:</div>
            <ul className="list-disc list-inside text-zinc-300 text-sm space-y-1">
              {abResult.issues_b.length > 0 ? abResult.issues_b.map((issue, idx) => (
                <li key={idx}>{issue}</li>
              )) : <li>No issues detected.</li>}
            </ul>
          </div>
        </div>
      </div>

      <div className="mt-6 p-4 rounded-3xl bg-zinc-950/60 border border-zinc-800 text-sm text-zinc-300">
        <p>{abResult.message}</p>
      </div>
    </div>
  );
}
