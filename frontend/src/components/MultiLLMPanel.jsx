import React from 'react';
import { Bot, ShieldAlert, Zap, LayoutList, Text, Clock, FlaskConical } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

const MODEL_COLORS = {
  Groq: { stroke: '#f97316', text: 'text-orange-500', dot: 'bg-orange-500' },
  Gemini: { stroke: '#3b82f6', text: 'text-blue-500', dot: 'bg-blue-500' },
  HuggingFace: { stroke: '#f59e0b', text: 'text-amber-500', dot: 'bg-amber-500' },
};

export default function MultiLLMPanel({ comparison }) {
  if (!comparison) return null;

  const getColor = (name) => MODEL_COLORS[name] || { stroke: '#a1a1aa', text: 'text-zinc-400', dot: 'bg-zinc-400' };

  return (
    <div className="space-y-8 animate-in mt-12 pt-8 border-t border-zinc-800 fade-in-0 duration-1000">
      
      {comparison.recommendation && (
        <div className="bg-emerald-950/30 border border-emerald-500/20 rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden">
          <div className="flex items-center gap-2 mb-3">
            <Zap size={20} className="text-emerald-400" />
            <h3 className="text-xl font-bold text-emerald-100">Best Model Suggestion</h3>
          </div>
          <div className="flex items-center gap-3">
             <span className={`px-4 py-2 rounded-lg font-bold bg-zinc-900 border border-zinc-700 ${getColor(comparison.recommendation.best_model).text}`}>
                {comparison.recommendation.best_model}
             </span>
             <p className="text-sm text-zinc-300 leading-relaxed">
               {comparison.recommendation.reason}
             </p>
          </div>
        </div>
      )}

      <div className="glass rounded-[var(--radius)] p-6 shadow-2xl relative overflow-hidden">
        <h2 className="text-2xl font-bold gradient-text mb-6">LLM Behavior Comparison</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-zinc-300">
            <thead className="text-xs uppercase bg-zinc-900/50 text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="px-6 py-4 rounded-tl-lg">Model</th>
                <th className="px-6 py-4">Metrics (V / S / C / Sf)</th>
                <th className="px-6 py-4 rounded-tr-lg">Behavior Profile</th>
              </tr>
            </thead>
            <tbody>
              {comparison.models.map((model, idx) => (
                <tr key={idx} className="border-b border-zinc-800/50 hover:bg-zinc-800/30 transition-colors">
                  <td className="px-6 py-5 font-bold text-white">
                    <div className="flex items-center gap-3">
                      <Bot className={getColor(model.model_name).text} />
                      <div>
                        <div>{model.model_name}</div>
                        <div className={`text-[10px] font-medium mt-0.5 flex items-center gap-1 ${model.source === 'real' ? 'text-emerald-400' : 'text-zinc-500'}`}>
                          <FlaskConical size={10} />
                          {model.source === 'real' ? 'Live API' : 'Mock (no key)'}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex flex-wrap gap-4 text-xs font-medium font-mono text-zinc-400">
                      <span className="flex items-center gap-1" title="Verbosity"><Text size={14}/> {model.behavior_stats.verbosity.toFixed(2)}</span>
                      <span className="flex items-center gap-1" title="Structure"><LayoutList size={14}/> {model.behavior_stats.structure.toFixed(2)}</span>
                      <span className="flex items-center gap-1" title="Creativity"><Zap size={14}/> {model.behavior_stats.creativity.toFixed(2)}</span>
                      <span className="flex items-center gap-1" title="Safety"><ShieldAlert size={14}/> {model.behavior_stats.safety.toFixed(2)}</span>
                      {model.latency_ms > 0 && (
                        <span className="flex items-center gap-1 text-cyan-400" title="Latency"><Clock size={14}/> {model.latency_ms}ms</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-5 text-sm">
                    <div className="flex flex-wrap gap-2 mb-3">
                       {model.behavior_labels.map((label, i) => (
                         <span key={i} className="bg-zinc-900 border border-zinc-700 px-3 py-1.5 rounded-full text-xs font-medium text-zinc-300">{label}</span>
                       ))}
                    </div>
                    <div className="text-zinc-400 mt-2 bg-zinc-900/40 p-3 rounded-lg border border-zinc-800/50 whitespace-pre-wrap max-h-48 overflow-y-auto font-mono text-xs">
                      {model.response_text}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 items-stretch">
        <div className="glass rounded-[var(--radius)] p-6 h-full flex flex-col">
          <h3 className="text-lg font-bold text-white mb-4">Why do they differ?</h3>
          <ul className="space-y-4 flex-grow">
            {comparison.explanation.map((exp, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-zinc-300 bg-zinc-900/50 p-4 rounded-lg border border-zinc-800">
                <span className="leading-snug">{exp}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="glass rounded-[var(--radius)] p-6 h-full min-h-[350px] flex flex-col">
          <h3 className="text-lg font-bold text-white mb-4">Behavioral Radar</h3>
          <div className="flex-1 w-full min-h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" 
                data={[
                  { metric: "Verbosity", ...comparison.models.reduce((acc, m) => ({...acc, [m.model_name]: m.behavior_stats.verbosity * 100}), {}) },
                  { metric: "Structure", ...comparison.models.reduce((acc, m) => ({...acc, [m.model_name]: m.behavior_stats.structure * 100}), {}) },
                  { metric: "Creativity", ...comparison.models.reduce((acc, m) => ({...acc, [m.model_name]: m.behavior_stats.creativity * 100}), {}) },
                  { metric: "Safety", ...comparison.models.reduce((acc, m) => ({...acc, [m.model_name]: m.behavior_stats.safety * 100}), {}) }
                ]}
              >
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }} />
                {comparison.models.map((m) => (
                  <Radar key={m.model_name} name={m.model_name} dataKey={m.model_name} stroke={getColor(m.model_name).stroke} fill={getColor(m.model_name).stroke} fillOpacity={0.2} />
                ))}
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center flex-wrap gap-4 mt-4 text-sm font-semibold">
             {comparison.models.map((m) => (
               <span key={m.model_name} className={`flex items-center gap-1 ${getColor(m.model_name).text}`}>
                 <span className={`w-3 h-3 rounded-full ${getColor(m.model_name).dot}`}></span> {m.model_name}
               </span>
             ))}
          </div>
        </div>
      </div>
    </div>
  );
}
