import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Database } from 'lucide-react';
import { saveDatasetEntry, getDatasetEntries } from '../api/client';

export default function DatasetPanel() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    prompt: '',
    expected_keywords: '',
    expected_format: '',
    ideal_length: 100,
    version: 'v1'
  });

  useEffect(() => {
    loadDataset();
  }, []);

  const loadDataset = async () => {
    try {
      setLoading(true);
      const data = await getDatasetEntries();
      setEntries(data || []);
    } catch (error) {
      console.error('Failed to load dataset:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddEntry = async () => {
    if (!formData.prompt.trim()) {
      alert('Prompt is required');
      return;
    }

    try {
      setLoading(true);
      const keywords = formData.expected_keywords
        ? formData.expected_keywords.split(',').map(k => k.trim())
        : [];
      
      const result = await saveDatasetEntry(
        formData.prompt,
        keywords,
        formData.expected_format || null,
        parseInt(formData.ideal_length) || 100,
        formData.version
      );

      if (result.success) {
        setFormData({
          prompt: '',
          expected_keywords: '',
          expected_format: '',
          ideal_length: 100,
          version: 'v1'
        });
        await loadDataset();
      }
    } catch (error) {
      console.error('Failed to add entry:', error);
      alert('Failed to add dataset entry');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass rounded-[var(--radius)] p-6 space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Database size={24} className="text-purple-400" />
        <h2 className="text-2xl font-bold gradient-text">Dataset Management</h2>
      </div>

      {/* Add New Entry Form */}
      <div className="bg-zinc-900/50 rounded-lg p-5 border border-zinc-800 space-y-4">
        <h3 className="text-lg font-semibold text-zinc-100">Add Golden Entry</h3>
        
        <div>
          <label className="text-sm font-medium text-zinc-400 block mb-2">Prompt</label>
          <textarea
            value={formData.prompt}
            onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
            placeholder="Enter a prompt to add to the golden dataset..."
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500"
            rows="3"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-zinc-400 block mb-2">Expected Keywords (comma-separated)</label>
            <input
              type="text"
              value={formData.expected_keywords}
              onChange={(e) => setFormData({ ...formData, expected_keywords: e.target.value })}
              placeholder="e.g., api, database, authentication"
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-zinc-400 block mb-2">Expected Format</label>
            <select
              value={formData.expected_format}
              onChange={(e) => setFormData({ ...formData, expected_format: e.target.value })}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
            >
              <option value="">None</option>
              <option value="bullet">Bullet Points</option>
              <option value="json">JSON</option>
            </select>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-zinc-400 block mb-2">Ideal Length (words)</label>
            <input
              type="number"
              value={formData.ideal_length}
              onChange={(e) => setFormData({ ...formData, ideal_length: e.target.value })}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white focus:outline-none focus:border-purple-500"
              min="1"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-zinc-400 block mb-2">Version</label>
            <input
              type="text"
              value={formData.version}
              onChange={(e) => setFormData({ ...formData, version: e.target.value })}
              placeholder="v1"
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <button
          onClick={handleAddEntry}
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all"
        >
          <Plus size={18} />
          {loading ? 'Adding...' : 'Add Entry'}
        </button>
      </div>

      {/* Dataset Entries Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-zinc-100">Existing Entries ({entries.length})</h3>
        
        {entries.length === 0 ? (
          <div className="bg-zinc-900/50 rounded-lg p-8 text-center border border-zinc-800">
            <Database size={32} className="mx-auto text-zinc-600 mb-2" />
            <p className="text-zinc-400">No dataset entries yet. Add one to get started!</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {entries.map((entry, idx) => (
              <div
                key={idx}
                className="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800 hover:border-zinc-700 transition-all"
              >
                <div className="flex justify-between items-start gap-4">
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-sm font-medium mb-1 truncate">{entry.prompt}</p>
                    <div className="flex flex-wrap gap-2 text-xs text-zinc-400">
                      {entry.expected_keywords && entry.expected_keywords.length > 0 && (
                        <span className="bg-blue-500/10 text-blue-300 px-2 py-1 rounded">
                          Keywords: {entry.expected_keywords.join(', ')}
                        </span>
                      )}
                      {entry.expected_format && (
                        <span className="bg-purple-500/10 text-purple-300 px-2 py-1 rounded">
                          Format: {entry.expected_format}
                        </span>
                      )}
                      {entry.ideal_length && (
                        <span className="bg-green-500/10 text-green-300 px-2 py-1 rounded">
                          Length: {entry.ideal_length} words
                        </span>
                      )}
                      {entry.version && (
                        <span className="bg-zinc-700/50 text-zinc-300 px-2 py-1 rounded">
                          {entry.version}
                        </span>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      // TODO: Implement delete functionality when backend supports it
                      console.log('Delete:', entry);
                    }}
                    className="text-red-400 hover:text-red-300 transition-colors p-1"
                    title="Delete entry"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
