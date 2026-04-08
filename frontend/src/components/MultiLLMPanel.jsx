import React from 'react';
import { Bot, Zap, Text, Clock, Brain, Hourglass } from 'lucide-react';
import LatencyChart from './LatencyChart';

const MODEL_COLORS = {
  Groq: { text: 'text-orange-500', dot: 'bg-orange-500' },
  Gemini: { text: 'text-blue-500', dot: 'bg-blue-500' },
  HuggingFace: { text: 'text-amber-500', dot: 'bg-amber-500' },
};

const getLatencyIndicator = (latencyMs) => {
  if (!latencyMs || latencyMs === 0) return { label: 'Unknown', icon: <Hourglass size={14}/>, color: 'text-zinc-500' };
  if (latencyMs < 150) return { label: 'Fast', icon: <Zap size={14}/>, color: 'text-emerald-400' };
  if (latencyMs <= 250) return { label: 'Medium', icon: <Brain size={14}/>, color: 'text-yellow-400' };
  return { label: 'Moderate', icon: <Hourglass size={14}/>, color: 'text-orange-400' };
};

export default function MultiLLMPanel({ comparison }) {
  if (!comparison || !comparison.responses) return null;

  const getColor = (name) => MODEL_COLORS[name] || { text: 'text-zinc-400', dot: 'bg-zinc-400' };

  const models = Object.keys(comparison.responses);

  return (
    <div className="space-y-8 animate-in mt-12 pt-8 border-t border-zinc-800 fade-in-0 duration-1000">
      
      {comparison.best_model && (
        <div className="bg-emerald-950/30 border border-emerald-500/20 rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden">
          <div className="flex items-center gap-2 mb-3">
            <Zap size={20} className="text-emerald-400" />
            <h3 className="text-xl font-bold text-emerald-100">Best Model Suggestion</h3>
          </div>
          <div className="flex items-center gap-3">
             <span className={`px-4 py-2 rounded-lg font-bold bg-zinc-900 border border-zinc-700 ${getColor(comparison.best_model).text}`}>
                {comparison.best_model}
             </span>
             <p className="text-sm text-zinc-300 leading-relaxed">
               Based on benchmark metrics and actual latency, this model provided the best trade-off.
             </p>
          </div>
        </div>
      )}

      <div className="glass rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden">
        <h2 className="text-2xl font-bold gradient-text mb-6">LLM Response Comparison</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-zinc-300">
            <thead className="text-xs uppercase bg-zinc-900/50 text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="px-6 py-4 rounded-tl-lg">Model</th>
                <th className="px-6 py-4">Metrics</th>
                <th className="px-6 py-4 rounded-tr-lg">Output text</th>
              </tr>
            </thead>
            <tbody>
              {models.map((modelName, idx) => {
                const latency = comparison.latency[modelName];
                const score = comparison.scores[modelName];
                const text = comparison.responses[modelName];
                const indicator = getLatencyIndicator(latency);

                return (
                  <tr key={idx} className="border-b border-zinc-800/50 hover:bg-zinc-800/30 transition-colors">
                    <td className="px-6 py-5 font-bold text-white align-top">
                      <div className="flex items-center gap-3">
                        <Bot className={getColor(modelName).text} />
                        <div>
                          <div>{modelName}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-5 align-top flex-col gap-2 min-w-[200px]">
                      <div className="flex flex-col gap-2 text-xs font-medium font-mono text-zinc-400">
                        <span className="flex items-center gap-2 bg-zinc-900/50 p-2 rounded-md border border-zinc-800">
                           <span className="text-zinc-500">Score:</span> 
                           <span className="text-white font-bold">{score}/10</span>
                        </span>
                        
                        <span className="flex items-center justify-between gap-2 bg-zinc-900/50 p-2 rounded-md border border-zinc-800 w-full">
                           <span className="flex items-center gap-1 text-cyan-400">
                             <Clock size={14}/> {latency}ms
                           </span>
                           <span className={`flex items-center gap-1 ${indicator.color}`}>
                             {indicator.icon} {indicator.label}
                           </span>
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-5 text-sm align-top">
                      <div className="text-zinc-400 bg-zinc-900/40 p-4 rounded-lg border border-zinc-800/50 whitespace-pre-wrap max-h-48 overflow-y-auto font-mono text-xs">
                        {text}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="glass rounded-[var(--radius)] p-6 shadow-2xl">
         <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
            <Clock className="text-cyan-400" size={20} />
            Response Time Visualization
         </h3>
         <p className="text-sm text-zinc-400 mb-4">Comparison of model inference latency in milliseconds.</p>
         <LatencyChart latencyData={comparison.latency} />
      </div>

    </div>
  );
}
