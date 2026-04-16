import React, { useState } from 'react';
import { Sparkles, Terminal, ShieldAlert } from 'lucide-react';
import InputBox from './components/InputBox';
import ScorePanel from './components/ScorePanel';
import IssuesPanel from './components/IssuesPanel';
import ComparisonPanel from './components/ComparisonPanel';
import MultiLLMPanel from './components/MultiLLMPanel';
import ABComparisonPanel from './components/ABComparisonPanel';
import FeedbackPanel from './components/FeedbackPanel';
import ABInputBox from './components/ABInputBox';
import PromptHistoryPanel from './components/PromptHistoryPanel';
import ApiStatusPanel from './components/ApiStatusPanel';
import { analyzePrompt, optimizePrompt, compareModels, abTestPrompts, submitFeedback, getPromptHistory, savePromptVersion } from './api/client';

function App() {
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [abResult, setAbResult] = useState(null);
  const [feedbackSent, setFeedbackSent] = useState(null);
  const [currentPrompt, setCurrentPrompt] = useState('');
  const [promptHistory, setPromptHistory] = useState([]);

  const handleAnalyze = async (promptText) => {
    setLoading(true);
    setEvaluation(null);
    setOptimization(null);
    setComparison(null);
    setPromptHistory([]);
    try {
      setCurrentPrompt(promptText);
      const evalData = await analyzePrompt(promptText);
      setEvaluation(evalData);
      
      const optData = await optimizePrompt(promptText);
      setOptimization(optData);
      
      const compData = await compareModels(promptText);
      setComparison(compData);
      const history = await getPromptHistory(promptText);
      setPromptHistory(history || []);
    } catch (error) {
      console.error("Failed to analyze prompt:", error);
      alert("Failed to connect to the analysis engine. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleABTest = async (promptA, promptB, expectedKeywords, expectedFormat, idealLength) => {
    setLoading(true);
    setAbResult(null);
    try {
      const result = await abTestPrompts(promptA, promptB, expectedKeywords, expectedFormat, idealLength);
      setAbResult(result);
    } catch (error) {
      console.error('Failed to run A/B test:', error);
      alert('Failed to run A/B comparison. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback, score = null, comment = null) => {
    if (!evaluation) return;
    try {
      const result = await submitFeedback(evaluation.original_prompt, feedback, score, comment);
      setFeedbackSent(result.success ? 'Thanks for your feedback!' : 'Feedback failed to save.');
    } catch (error) {
      console.error('Feedback submission failed:', error);
      alert('Could not submit feedback.');
    }
  };

  const handleSaveVersion = async (promptText, version) => {
    if (!promptText) return;
    try {
      const result = await savePromptVersion(promptText, version);
      if (result.success) {
        const history = await getPromptHistory(promptText);
        setPromptHistory(history || []);
      }
    } catch (error) {
      console.error('Failed to save prompt version:', error);
      alert('Could not save prompt version.');
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-5xl mx-auto space-y-8 animate-in fade-in-0 duration-1000">
      {/* Header */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-12 text-center md:text-left gap-4">
        <div>
          <h1 className="text-3xl md:text-5xl font-black tracking-tight flex items-center justify-center md:justify-start gap-3">
            Prompt<span className="gradient-text">Evaluator</span>
            <Sparkles className="text-purple-400" size={32} />
          </h1>
          <p className="text-zinc-400 mt-2 text-lg">Analyze and optimize your LLM prompts scientifically.</p>
        </div>
        <div className="bg-zinc-800/50 border border-zinc-700 rounded-full px-4 py-2 flex items-center gap-2 text-sm text-zinc-300">
          <Terminal size={14} className="text-green-400"/>
          <span>System Online</span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 gap-8">
        <ApiStatusPanel />
        <InputBox onAnalyze={handleAnalyze} isLoading={loading} />
        <ABInputBox onRunABTest={handleABTest} isLoading={loading} />

        {loading && (
          <div className="glass rounded-[var(--radius)] py-20 flex flex-col justify-center items-center gap-4 animate-in fade-in">
            <div className="w-12 h-12 border-4 border-blue-500/20 border-t-purple-500 rounded-full animate-spin"></div>
            <p className="text-zinc-400 font-medium animate-pulse">Running mathematical models...</p>
          </div>
        )}

        {!loading && evaluation && (
          <div className="space-y-8 animate-in slide-in-from-bottom-8 fade-in-0 duration-700 fill-mode-both">
            <ScorePanel score={evaluation.score} metrics={evaluation.metrics} />
            
            <div className="grid md:grid-cols-2 gap-8">
              <IssuesPanel issues={evaluation.issues} />
              
              <div className="glass rounded-[var(--radius)] p-6 border-l-4 border-l-blue-500/50">
                <h2 className="text-xl font-bold text-zinc-100 mb-4">Analysis Insights</h2>
                
                {/* Intent and Template Badges */}
                {(evaluation.intent || evaluation.template) && (
                  <div className="flex flex-wrap gap-3 mb-4">
                    {evaluation.intent && (
                      <div className="flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 text-sm">
                        <span className="text-zinc-400">Intent:</span>
                        <span className="font-semibold text-blue-300">{evaluation.intent}</span>
                      </div>
                    )}
                    {evaluation.template && (
                      <div className="flex items-center gap-2 bg-green-500/10 border border-green-500/20 rounded-full px-4 py-1.5 text-sm">
                        <span className="text-zinc-400">Template:</span>
                        <span className="font-semibold text-green-300">{evaluation.template}</span>
                      </div>
                    )}
                  </div>
                )}
                
                <div className="bg-zinc-900/50 rounded-lg p-5 border border-zinc-800 flex justify-between items-center h-28">
                  <div>
                    <div className="text-xs font-bold text-zinc-500 uppercase tracking-wide mb-2">Likely Form</div>
                    <div className="text-xl font-semibold text-white">{evaluation.response_prediction.type}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-bold text-zinc-500 uppercase tracking-wide mb-2">Confidence</div>
                    <div className="text-xl font-bold gradient-text">
                      {Math.round(evaluation.response_prediction.confidence * 100)}%
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {optimization && optimization.suggestions && optimization.suggestions.length > 0 && (
              <ComparisonPanel 
                original={optimization.original_prompt}
                suggestions={optimization.suggestions}
              />
            )}

            {comparison && (
               <>
                 {comparison.is_malicious && (
                   <div className="bg-red-950/40 border-l-4 border-l-red-500 p-4 rounded-r-lg mb-6 flex items-start gap-3">
                     <ShieldAlert className="text-red-500 mt-1" size={20} />
                     <div>
                       <h3 className="text-red-400 font-bold">Warning: Potential Prompt Injection Detected</h3>
                       <p className="text-red-300 text-sm">{comparison.reason || "This prompt contains patterns associated with jailbreaks or system instruction overrides."}</p>
                     </div>
                   </div>
                 )}
                 <MultiLLMPanel comparison={comparison} />
                <FeedbackPanel onFeedback={handleFeedback} feedbackSent={feedbackSent} />
               </>
            )}
          </div>
        )}
        {abResult && (
          <ABComparisonPanel abResult={abResult} />
        )}
        {promptHistory && promptHistory.length >= 0 && (
          <PromptHistoryPanel
            promptHistory={promptHistory}
            onLoadVersion={(promptText) => handleAnalyze(promptText)}
            onSaveVersion={handleSaveVersion}
            currentPrompt={currentPrompt}
          />
        )}
      </div>
    </div>
  );
}

export default App;
