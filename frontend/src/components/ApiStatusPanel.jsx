import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { CheckCircle2, XCircle, Loader2 } from 'lucide-react';

const statusIcons = {
  connected: <CheckCircle2 size={16} className="text-emerald-400 shrink-0" />,
  missing_key: <XCircle size={16} className="text-red-400 shrink-0" />,
};

const MODEL_COLORS = {
  Groq: 'text-orange-400',
  Gemini:  'text-blue-400',
  HuggingFace:    'text-amber-400',
};

export default function ApiStatusPanel() {
  const [statuses, setStatuses] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000/api/api-status')
      .then(r => setStatuses(r.data.statuses))
      .catch(() => setStatuses(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="glass rounded-[var(--radius)] px-5 py-3 flex items-center gap-2 text-sm text-zinc-400">
      <Loader2 size={14} className="animate-spin" /> Checking API status...
    </div>
  );

  if (!statuses) return null;

  return (
    <div className="glass rounded-[var(--radius)] p-5">
      <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-500 mb-4">API Key Status</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {Object.entries(statuses).map(([model, status]) => (
          <div key={model} className={`flex items-center gap-2 bg-zinc-900/60 rounded-lg px-3 py-2.5 border ${status === 'connected' ? 'border-emerald-500/20' : 'border-red-500/20'}`}>
            {statusIcons[status] || <XCircle size={16} className="text-zinc-500 shrink-0"/>}
            <div>
              <div className={`text-xs font-bold ${MODEL_COLORS[model] || 'text-zinc-300'}`}>{model}</div>
              <div className="text-[10px] text-zinc-500 capitalize">{status === 'connected' ? '✅ Connected' : '❌ Key Missing'}</div>
            </div>
          </div>
        ))}
      </div>
      <p className="text-[10px] text-zinc-600 mt-3">
        Models without API keys fall back to mock responses automatically.
        Add keys to <code className="text-zinc-400">backend/.env</code> to enable real calls.
      </p>
    </div>
  );
}
