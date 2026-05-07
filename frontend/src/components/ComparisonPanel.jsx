import React, { useState } from 'react';
import { ArrowRight, Copy, CheckCircle2 } from 'lucide-react';

export default function ComparisonPanel({ original, suggestions }) {

  const tabs = suggestions
    ? Object.entries(suggestions).map(([key, value]) => ({
        name: value.title || key,
        prompt: value.content || "",
        transformation_steps: value.why || []
      }))
    : [];

  const [activeTab, setActiveTab] = useState(0);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  if (!tabs.length) return null;

  const activeSuggestion = tabs[activeTab];

  return (
    <div className="glass rounded-[var(--radius)] p-6 space-y-6">

      <h2 className="text-xl font-bold gradient-text">
        Advanced Prompt Optimization
      </h2>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-zinc-800 pb-2 overflow-x-auto">
        {tabs.map((s, idx) => (
          <button
            key={idx}
            onClick={() => setActiveTab(idx)}
            className={`px-4 py-2 rounded-t-lg text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === idx
                ? 'bg-blue-600 text-white'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            }`}
          >
            {s.name}
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6 items-stretch">

        {/* LEFT */}
        <div className="space-y-4 flex flex-col h-full">

          <div className="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wide mb-2">
              Original Prompt
            </div>

            <p className="text-zinc-400 text-sm whitespace-pre-wrap">
              {original}
            </p>
          </div>

          <div className="flex justify-center -my-2 relative z-10 py-1">
            <div className="bg-blue-500/20 p-2 rounded-full border border-blue-500/30">
              <ArrowRight className="text-blue-400" size={16}/>
            </div>
          </div>

          <div className="bg-blue-900/10 rounded-lg p-5 border border-blue-500/30 relative group flex-grow">

            <div className="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-3 flex justify-between items-center">

              {activeSuggestion.name}

              <button
                onClick={() => copyToClipboard(activeSuggestion.prompt)}
                className="text-zinc-400 hover:text-white"
              >
                <Copy size={16} />
              </button>

            </div>

            <p className="text-white text-base font-medium leading-relaxed whitespace-pre-wrap">
              {activeSuggestion.prompt}
            </p>

          </div>

        </div>

        {/* RIGHT */}
        <div className="bg-zinc-900/80 rounded-lg p-5 border border-zinc-800">

          <h3 className="text-sm font-bold text-zinc-200 uppercase tracking-wider mb-4 border-b border-zinc-800 pb-2">
            Why this suggestion?
          </h3>

          <ul className="space-y-4">

            {activeSuggestion.transformation_steps?.map((step, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-zinc-300">

                <CheckCircle2
                  size={16}
                  className="text-emerald-500 mt-0.5 shrink-0"
                />

                <span>{step}</span>

              </li>
            ))}

          </ul>

        </div>

      </div>

    </div>
  );
}