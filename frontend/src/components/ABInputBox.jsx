import React, { useState } from 'react';
import { Send, Layers } from 'lucide-react';

export default function ABInputBox({ onRunABTest, isLoading }) {
  const [promptA, setPromptA] = useState('');
  const [promptB, setPromptB] = useState('');
  const [expectedKeywords, setExpectedKeywords] = useState('');
  const [expectedFormat, setExpectedFormat] = useState('');
  const [idealLength, setIdealLength] = useState(100);

  const handleRun = () => {
    if (!promptA.trim() || !promptB.trim()) return;
    onRunABTest(
      promptA,
      promptB,
      expectedKeywords.split(',').map((k) => k.trim()).filter(Boolean),
      expectedFormat || null,
      Number(idealLength) || 100
    );
  };

  return (
    <div className="glass rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-4">
          <Layers size={18} className="text-violet-400" />
          <h2 className="text-lg font-bold text-white">A/B Prompt Test</h2>
        </div>
        <div className="grid gap-4 lg:grid-cols-2">
          <textarea
            value={promptA}
            onChange={(e) => setPromptA(e.target.value)}
            className="w-full min-h-[120px] bg-zinc-800/50 text-white border border-zinc-700/50 rounded-lg p-4 focus:ring-2 focus:ring-violet-500 outline-none resize-none"
            placeholder="Prompt A"
          />
          <textarea
            value={promptB}
            onChange={(e) => setPromptB(e.target.value)}
            className="w-full min-h-[120px] bg-zinc-800/50 text-white border border-zinc-700/50 rounded-lg p-4 focus:ring-2 focus:ring-violet-500 outline-none resize-none"
            placeholder="Prompt B"
          />
        </div>
        <div className="grid gap-4 mt-4 sm:grid-cols-3">
          <input
            value={expectedKeywords}
            onChange={(e) => setExpectedKeywords(e.target.value)}
            className="bg-zinc-900 border border-zinc-800 rounded-lg p-3 text-zinc-200 focus:ring-2 focus:ring-violet-500 outline-none"
            placeholder="Expected keywords (comma separated)"
          />
          <input
            value={expectedFormat}
            onChange={(e) => setExpectedFormat(e.target.value)}
            className="bg-zinc-900 border border-zinc-800 rounded-lg p-3 text-zinc-200 focus:ring-2 focus:ring-violet-500 outline-none"
            placeholder="Expected format (bullet/json)"
          />
          <input
            type="number"
            value={idealLength}
            onChange={(e) => setIdealLength(e.target.value)}
            className="bg-zinc-900 border border-zinc-800 rounded-lg p-3 text-zinc-200 focus:ring-2 focus:ring-violet-500 outline-none"
            placeholder="Ideal length"
          />
        </div>
        <div className="mt-4 flex justify-end">
          <button
            onClick={handleRun}
            disabled={isLoading || !promptA.trim() || !promptB.trim()}
            className="flex items-center gap-2 px-6 py-3 bg-violet-600 text-white rounded-lg hover:bg-violet-500 disabled:opacity-50 transition-all duration-300"
          >
            {isLoading ? 'Running A/B...' : 'Run A/B Test'}
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
