import React, { useState } from 'react';
import { Send, Wand2 } from 'lucide-react';

export default function InputBox({ onAnalyze, isLoading }) {
  const [prompt, setPrompt] = useState("");

  const handleAnalyze = () => {
    if (prompt.trim()) onAnalyze(prompt);
  };

  return (
    <div className="glass rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div className="relative z-10">
        <label className="block text-sm font-medium text-zinc-400 mb-3 flex items-center gap-2">
          <Wand2 size={16} className="text-blue-500" />
          Enter your prompt below for analysis
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full h-40 bg-zinc-800/50 text-white border border-zinc-700/50 rounded-lg p-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none transition-all duration-300"
          placeholder="e.g., Explain Artificial Intelligence with examples..."
        />
        <div className="mt-4 flex justify-end">
          <button
            onClick={handleAnalyze}
            disabled={isLoading || !prompt.trim()}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-500 disabled:opacity-50 transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg shadow-blue-500/25 cursor-pointer"
          >
            {isLoading ? "Analyzing..." : "Analyze Prompt"}
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
