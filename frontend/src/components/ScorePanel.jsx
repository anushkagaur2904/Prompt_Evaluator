import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export default function ScorePanel({ score, metrics }) {
  const data = [
    { subject: 'Clarity', A: metrics.clarity * 100, fullMark: 100 },
    { subject: 'Specificity', A: metrics.specificity * 100, fullMark: 100 },
    { subject: 'Context', A: metrics.context * 100, fullMark: 100 },
    { subject: 'Instruction', A: metrics.instruction * 100, fullMark: 100 },
    { subject: 'Ambiguity', A: metrics.ambiguity * 100, fullMark: 100 },
  ];

  return (
    <div className="glass rounded-[var(--radius)] p-6 flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <h2 className="text-xl font-bold gradient-text mb-2">Prompt Score</h2>
        <div className="text-6xl font-black text-white mb-6 tracking-tight">
          {score} <span className="text-2xl text-zinc-500 font-medium">/ 10</span>
        </div>
        
        <div className="space-y-5">
          {Object.entries(metrics).map(([key, value]) => (
            <div key={key}>
              <div className="flex justify-between text-xs mb-1.5 uppercase tracking-wider text-zinc-400 font-semibold">
                <span>{key}</span>
                <span className="text-white">{Math.round(value * 100)}%</span>
              </div>
              <div className="w-full bg-zinc-800 rounded-full h-2.5 shadow-inner overflow-hidden">
                <div 
                  className={`h-full rounded-full transition-all duration-1000 ease-out ${key === 'ambiguity' ? 'bg-gradient-to-r from-red-500 to-orange-500' : 'bg-gradient-to-r from-blue-500 to-purple-500'}`}
                  style={{ width: `${value * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="flex-1 min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
            <PolarGrid stroke="rgba(255,255,255,0.1)" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 11, fontWeight: 600 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
            <Radar name="Metrics" dataKey="A" stroke="#3b82f6" fill="url(#colorGradient)" fillOpacity={0.6} />
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.8}/>
              </linearGradient>
            </defs>
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
