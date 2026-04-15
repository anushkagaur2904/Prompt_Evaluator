import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown } from 'lucide-react';

export default function FeedbackPanel({ onFeedback, feedbackSent }) {
  const [comment, setComment] = useState('');

  return (
    <div className="glass rounded-[var(--radius)] p-6 border border-sky-500/20 shadow-2xl mt-8">
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white">Human Feedback</h3>
            <p className="text-sm text-zinc-400">Signal if this prompt result was helpful for future regression tracking.</p>
          </div>
          {feedbackSent && (
            <span className="text-emerald-300 text-sm font-semibold">{feedbackSent}</span>
          )}
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => onFeedback('upvote', null, comment)}
            className="flex items-center gap-2 px-4 py-3 bg-emerald-600/95 hover:bg-emerald-500 rounded-xl text-white transition"
          >
            <ThumbsUp size={18} />
            Helpful
          </button>
          <button
            onClick={() => onFeedback('downvote', null, comment)}
            className="flex items-center gap-2 px-4 py-3 bg-red-600/95 hover:bg-red-500 rounded-xl text-white transition"
          >
            <ThumbsDown size={18} />
            Needs Improvement
          </button>
        </div>

        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Optional feedback comment..."
          className="w-full min-h-[100px] bg-zinc-900 border border-zinc-800 rounded-3xl p-4 text-zinc-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
        />
      </div>
    </div>
  );
}
