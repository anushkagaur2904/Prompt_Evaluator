import React, { useState, useEffect } from 'react';
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

  // 🌙 THEME STATE
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved) setTheme(saved);
  }, []);

  useEffect(() => {
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

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
      alert("Backend not running!");
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
      console.error('AB test failed:', error);
      alert('A/B test failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback, score = null, comment = null) => {
    if (!evaluation) return;
    try {
      const result = await submitFeedback(evaluation.original_prompt, feedback, score, comment);
      setFeedbackSent(result.success ? 'Thanks!' : 'Failed');
    } catch (error) {
      alert('Feedback error');
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
      alert('Save failed');
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-5xl mx-auto space-y-8">

      {/* HEADER */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-12 gap-4">

        <div>
          <h1 className="text-3xl md:text-5xl font-black flex items-center gap-3">
            Prompt
            <span className={theme === "dark" ? "gradient-text" : "light-gradient"}>
              Evaluator
            </span>
            <Sparkles size={32} />
          </h1>

          <p className="mt-2 text-lg">
            Analyze and optimize your LLM prompts scientifically.
          </p>
        </div>

        {/* Toggle + Status */}
        <div className="flex items-center gap-3">

          <button
            onClick={toggleTheme}
            className="px-3 py-2 rounded-full text-sm bg-zinc-700 text-white hover:opacity-80"
          >
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>

          <div className="bg-zinc-800 border rounded-full px-4 py-2 flex items-center gap-2 text-sm">
            <Terminal size={14} className="text-green-400"/>
            <span>System Online</span>
          </div>
        </div>

      </header>

      {/* MAIN */}
      <div className="grid gap-8">
        <ApiStatusPanel />
        <InputBox onAnalyze={handleAnalyze} isLoading={loading} />
        <ABInputBox onRunABTest={handleABTest} isLoading={loading} />

        {loading && (
          <div className="py-20 flex flex-col items-center gap-4">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-purple-500 rounded-full animate-spin"></div>
            <p>Processing...</p>
          </div>
        )}

        {!loading && evaluation && (
          <div className="space-y-8">
            <ScorePanel score={evaluation.score} metrics={evaluation.metrics} />

            <div className="grid md:grid-cols-2 gap-8">
              <IssuesPanel issues={evaluation.issues} />

              <div className="p-6 border-l-4 border-blue-500">
                <h2 className="text-xl font-bold mb-4">Prediction</h2>
                <div className="p-5 flex justify-between">
                  <div>{evaluation.response_prediction.type}</div>
                  <div>
                    {Math.round(evaluation.response_prediction.confidence * 100)}%
                  </div>
                </div>
              </div>
            </div>

            {optimization && (
              <ComparisonPanel
                original={optimization.original_prompt}
                suggestions={optimization.suggestions}
              />
            )}

            {comparison && (
              <>
                {comparison.is_malicious && (
                  <div className="border-l-4 border-red-500 p-4">
                    <ShieldAlert />
                    <p>{comparison.reason}</p>
                  </div>
                )}

                <MultiLLMPanel comparison={comparison} />
                <FeedbackPanel onFeedback={handleFeedback} feedbackSent={feedbackSent} />
              </>
            )}
          </div>
        )}

        {abResult && <ABComparisonPanel abResult={abResult} />}

        <PromptHistoryPanel
          promptHistory={promptHistory}
          onLoadVersion={(p) => handleAnalyze(p)}
          onSaveVersion={handleSaveVersion}
          currentPrompt={currentPrompt}
        />
      </div>
    </div>
  );
}

export default App;
