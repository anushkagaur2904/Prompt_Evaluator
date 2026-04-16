import React, { useState } from 'react';
import { ArrowRight, Copy, CheckCircle2, Globe, Lightbulb } from 'lucide-react';

export default function ComparisonPanel({ original, suggestions }) {
  const [activeTab, setActiveTab] = useState(0);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  if (!suggestions || suggestions.length === 0) return null;

  const activeSuggestion = suggestions[activeTab];

  return (
    <div className="glass rounded-[var(--radius)] p-6 space-y-6">
      <h2 className="text-xl font-bold gradient-text">Advanced Prompt Optimization</h2>

      {/* Domain + Intent + Template Detection Banner */}
      {(activeSuggestion.domain || activeSuggestion.intent || activeSuggestion.template) && (
        <div className="flex flex-wrap gap-3">
          {activeSuggestion.intent && (
            <div className="flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 text-sm">
              <Lightbulb size={14} className="text-blue-400" />
              <span className="text-zinc-400">Intent:</span>
              <span className="font-semibold text-blue-300">{activeSuggestion.intent}</span>
            </div>
          )}
          {activeSuggestion.template && (
            <div className="flex items-center gap-2 bg-green-500/10 border border-green-500/20 rounded-full px-4 py-1.5 text-sm">
              <CheckCircle2 size={14} className="text-green-400" />
              <span className="text-zinc-400">Template:</span>
              <span className="font-semibold text-green-300">{activeSuggestion.template}</span>
            </div>
          )}
          {activeSuggestion.domain && (
            <div className="flex items-center gap-2 bg-purple-500/10 border border-purple-500/20 rounded-full px-4 py-1.5 text-sm">
              <Globe size={14} className="text-purple-400" />
              <span className="text-zinc-400">Domain:</span>
              <span className="font-semibold text-purple-300">{activeSuggestion.domain}</span>
            </div>
          )}
        </div>
      )}
      
      {/* Top 3 Selection Tabs */}
      <div className="flex gap-2 border-b border-zinc-800 pb-2 overflow-x-auto">
        {suggestions.map((s, idx) => (
          <button
            key={idx}
            onClick={() => setActiveTab(idx)}
            className={`px-4 py-2 rounded-t-lg text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === idx 
                ? 'bg-blue-600 text-white' 
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            }`}
          >
            {s.name} Version
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6 items-stretch">
        {/* Left Side: Before -> After */}
        <div className="space-y-4 flex flex-col h-full">
          <div className="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wide mb-2">Original Prompt</div>
            <p className="text-zinc-400 text-sm whitespace-pre-wrap">{original}</p>
          </div>
          
          <div className="flex justify-center -my-2 relative z-10 py-1">
            <div className="bg-blue-500/20 p-2 rounded-full border border-blue-500/30">
              <ArrowRight className="text-blue-400" size={16}/>
            </div>
          </div>

          <div className="bg-blue-900/10 rounded-lg p-5 border border-blue-500/30 relative group shadow-[0_0_15px_rgba(59,130,246,0.1)] flex-grow">
            <div className="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-3 flex justify-between items-center">
              {activeSuggestion.name} Suggestion
              <button 
                onClick={() => copyToClipboard(activeSuggestion.prompt)}
                className="text-zinc-400 hover:text-white transition-colors p-1"
                title="Copy to clipboard"
              >
                <Copy size={16} />
              </button>
            </div>
            <p className="text-white text-base font-medium leading-relaxed whitespace-pre-wrap">
              {activeSuggestion.prompt}
            </p>
          </div>
        </div>

        {/* Right Side: Why this suggestion? (Transformation steps) */}
        <div className="bg-zinc-900/80 rounded-lg p-5 border border-zinc-800 h-full flex flex-col">
          <h3 className="text-sm font-bold text-zinc-200 uppercase tracking-wider mb-4 border-b border-zinc-800 pb-2">
            Why this suggestion?
          </h3>
          <ul className="space-y-4">
            {activeSuggestion.transformation_steps.map((step, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-zinc-300">
                <CheckCircle2 size={16} className="text-emerald-500 mt-0.5 shrink-0" />
                <span className="leading-snug flex-grow">{step}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
