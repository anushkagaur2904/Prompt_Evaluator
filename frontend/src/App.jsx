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

import {
  analyzePrompt,
  optimizePrompt,
  compareModels,
  abTestPrompts,
  submitFeedback,
  getPromptHistory,
  savePromptVersion,
  deletePromptHistory
} from './api/client';

function App() {
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [abResult, setAbResult] = useState(null);
  const [feedbackSent, setFeedbackSent] = useState(null);
  const [currentPrompt, setCurrentPrompt] = useState('');
  const [promptHistory, setPromptHistory] = useState([]);

  // 🌙 THEME
  //const [theme, setTheme] = useState("dark");

  //useEffect(() => {
  //  document.body.classList.remove("light", "dark");
  //  document.body.classList.add(theme);
  //}, [theme]);

  //useEffect(() => {
  //  const saved = localStorage.getItem("theme");
  //  if (saved) setTheme(saved);
  //}, []);

  //useEffect(() => {
  //  localStorage.setItem("theme", theme);
  //}, [theme]);

  //const toggleTheme = () => {
  //  setTheme(theme === "dark" ? "light" : "dark");
  //};

  // 🎯 Prediction color helper
  const getPredictionColor = (label) => {
    switch (label) {
      case "Excellent":
        return "text-green-400";
      case "Good":
        return "text-blue-400";
      case "Average":
        return "text-yellow-400";
      default:
        return "text-red-400";
    }
  };

  // ---------------- API ----------------

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
      //setPromptHistory(history || []);
      //setPromptHistory(history.history || []);
      setPromptHistory(
        Array.isArray(history?.history)
        ? history.history
        : []
      );

    } catch (error) {
      console.error(error);
      alert("Backend not running!");
    } finally {
      setLoading(false);
    }
  };

  const handleABTest = async (promptA, promptB, expectedKeywords, expectedFormat, idealLength) => {
    setLoading(true);
    setAbResult(null);

    try {
      const result = await abTestPrompts(
        promptA,
        promptB,
        expectedKeywords,
        expectedFormat,
        idealLength
      );
      setAbResult(result);
    } catch {
      alert("A/B test failed");
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback, score = null, comment = null) => {
    if (!evaluation) return;

    try {
      const result = await submitFeedback(
        evaluation.original_prompt,
        feedback,
        score,
        comment
      );

      setFeedbackSent(result.success ? "Thanks!" : "Failed");
    } catch {
      alert("Feedback error");
    }
  };

  const handleSaveVersion = async (promptText, version) => {
    try {
      
      const result = await savePromptVersion(
        promptText,
        version
      );

      if (result.success) {
        
        const historyResponse = await getPromptHistory(
          promptText
        );

        setPromptHistory(
          Array.isArray(historyResponse?.history)
          ? historyResponse.history
          : []
        );

        alert("Version saved successfully!");
      }
    } catch (error) {
      console.error(error);

      alert("Save failed");
    }
  }

  const handleDeleteHistory = async (id) => {
    try {
      const result = await deletePromptHistory(id);
      
      if (result.success) {
        setPromptHistory(prev =>
          prev.filter(item => item.id !== id)
        );
        
        alert("Prompt deleted successfully!");
      }
    
    } catch (error) {
      console.error(error);
      alert("Delete failed");
    }
  };

  // ---------------- UI ----------------

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-5xl mx-auto space-y-8 bg-[var(--background)] text-[var(--foreground)]">
    
      {/* HEADER */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-12 gap-4">

        <div>
          <h1 className="text-3xl md:text-5xl font-black flex items-center gap-3">
            Prompt
            <span className="gradient-text">
              Evaluator
            </span>
            <Sparkles size={28} />
          </h1>

          <p className="mt-2 text-lg text-[var(--muted-foreground)]">
            Analyze and optimize your LLM prompts scientifically.
          </p>
        </div>

        {/* Toggle + Status */}
        <div className="flex items-center gap-3">

          <div
            className="rounded-full px-4 py-2 flex items-center gap-2 text-sm"
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)"
            }}
          >
            <Terminal size={14} className="text-green-500" />
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
            <p className="text-[var(--muted-foreground)]">
              Processing...
            </p>
          </div>
        )}

        {!loading && evaluation && (
          <div className="space-y-8">

            {/* SCORE */}
            <ScorePanel score={evaluation.score} metrics={evaluation.metrics} />

            {/* ISSUES + PREDICTION */}
            <div className="grid md:grid-cols-2 gap-8">

              <IssuesPanel issues={evaluation.issues} />

              {/* ✅ FIXED PREDICTION */}
              <div className="p-6 border-l-4 border-blue-500">
                <h2 className="text-xl font-bold mb-4">Prediction</h2>

                {(() => {
                  const prediction =
                    evaluation.prediction ||
                    evaluation.response_prediction ||
                    {};

                  const label = prediction.label || prediction.type || "Unknown";
                  const confidence = prediction.confidence || 0;

                  return (
                    <div className="p-5 flex justify-between items-center">
                      <div className={`text-lg font-semibold ${getPredictionColor(label)}`}>
                        {label}
                      </div>

                      <div className="text-sm text-[var(--muted-foreground)]">
                        {confidence}%
                      </div>
                    </div>
                  );
                })()}
              </div>

            </div>

            {/* OPTIMIZATION */}
            {optimization && (
              <ComparisonPanel
                original={optimization.original_prompt}
                suggestions={optimization.suggestions}
              />
            )}

            {/* MODEL COMPARISON */}
            {comparison && (
              <>
                {comparison.is_malicious && (
                  <div className="border-l-4 border-red-500 p-4 flex gap-2">
                    <ShieldAlert />
                    <p>{comparison.reason}</p>
                  </div>
                )}

                <MultiLLMPanel comparison={comparison} />

                <FeedbackPanel
                  onFeedback={handleFeedback}
                  feedbackSent={feedbackSent}
                />
              </>
            )}

          </div>
        )}

        {abResult && <ABComparisonPanel abResult={abResult} />}

        <PromptHistoryPanel
        promptHistory={promptHistory}
        onLoadVersion={(p) => handleAnalyze(p)}
        onSaveVersion={handleSaveVersion}
        onDeleteVersion={handleDeleteHistory}
        currentPrompt={currentPrompt}
        />

      </div>
    </div>
  );
}

export default App;