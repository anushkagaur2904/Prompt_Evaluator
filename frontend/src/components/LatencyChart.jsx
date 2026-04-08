import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const MODEL_COLORS = {
  Groq: '#f97316',
  Gemini: '#3b82f6',
  HuggingFace: '#f59e0b',
};

export default function LatencyChart({ latencyData }) {
  const data = Object.keys(latencyData).map(model => ({
    name: model,
    latency: latencyData[model]
  }));

  return (
    <div className="w-full h-64 mt-6">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" tick={{fill: '#a1a1aa'}} axisLine={false} tickLine={false} />
          <YAxis tick={{fill: '#a1a1aa'}} axisLine={false} tickLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff' }}
            cursor={{fill: 'rgba(255,255,255,0.05)'}}
            formatter={(value) => [`${value} ms`, 'Latency']}
          />
          <Bar dataKey="latency" radius={[6, 6, 0, 0]} maxBarSize={60}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={MODEL_COLORS[entry.name] || '#a1a1aa'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
