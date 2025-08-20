// pages/index.jsx
import { useEffect, useRef, useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Button,
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
  Textarea,
  Slider,
} from "../components/ui";
import { Play, Pause, RotateCcw, Loader2 } from "lucide-react";
import Board from "../components/Board";
import { parseInitialState, PRESET_STATES, matrixToString, isSolvable } from "../utils/parseState";

export default function Home() {
  // form state
  const [algorithm, setAlgorithm] = useState("astar");
  const [heuristic, setHeuristic] = useState("manhattan");
  const [initialInput, setInitialInput] = useState("1 2 3\n4 5 6\n7 0 8");
  const [error, setError] = useState("");

  // result state
  const [isSolving, setIsSolving] = useState(false);
  const [board, setBoard] = useState([[1,2,3],[4,5,6],[7,0,8]]);
  const [actionsList, setActionsList] = useState([]); // [{board: [[...]], move:"...", heuristic: n}, ...]
  const [metrics, setMetrics] = useState({ moves: 0, time: 0, nodes_explored: 0 });

  // playback
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [speed, setSpeed] = useState(800); // ms
  const intervalRef = useRef(null);

  // preset handling
  const handlePresetChange = (preset) => {
    if (preset && PRESET_STATES[preset]) {
      setInitialInput(matrixToString(PRESET_STATES[preset]));
      setBoard(PRESET_STATES[preset]);
      // Clear previous results
      setActionsList([]);
      setMetrics({ moves: 0, time: 0, nodes_explored: 0 });
      setCurrentStep(0);
      setIsPlaying(false);
      setError("");
    }
  };

  // parse & call backend
  async function callSolveApi(payload) {
    // POST to /api/solve (backend Python). Backend must accept JSON per spec.
    const res = await fetch("/api/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`Server error: ${res.status} ${txt}`);
    }
    return res.json();
  }

  async function handleSolve({ showStepByStep = false } = {}) {
    setError("");
    const parsed = parseInitialState(initialInput);
    if (!parsed.ok) {
      setError(parsed.error);
      return;
    }

    // Check if solvable
    if (!isSolvable(parsed.state)) {
      setError("This puzzle configuration is not solvable!");
      return;
    }

    const payload = {
      algorithm,
      heuristic,
      initial: parsed.state, // e.g. [[1,2,3],[4,5,6],[7,8,0]]
      mode: showStepByStep ? "steps" : "final",
    };

    setIsSolving(true);
    setIsPlaying(false);
    setCurrentStep(0);
    clearInterval(intervalRef.current);

    try {
      const json = await callSolveApi(payload);
      if (!json.success) {
        setError(json.message || "No solution / error from backend");
        setIsSolving(false);
        return;
      }

      // update UI
      setActionsList(json.steps || []);
      setMetrics({
        moves: json.metrics?.moves ?? (json.steps?.length ? json.steps.length - 1 : 0),
        time: json.metrics?.time ?? 0,
        nodes_explored: json.metrics?.nodes_explored ?? 0,
      });

      // If "Solve Now" => show final state
      if (!showStepByStep) {
        const final = (json.steps && json.steps.length) ? json.steps[json.steps.length - 1].board : parsed.state;
        setBoard(final);
        setCurrentStep((json.steps?.length ? json.steps.length - 1 : 0));
      } else {
        // "Show Solution": start playback at step 0 but don't autoplay unless user hits Play
        const first = json.steps?.[0]?.board ?? parsed.state;
        setBoard(first);
        setCurrentStep(0);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Error contacting backend. Make sure the Python API is running on port 8000.");
    } finally {
      setIsSolving(false);
    }
  }

  // Playback controls
  function handlePlay() {
    if (!actionsList.length) return;
    setIsPlaying(true);
  }

  function handlePause() {
    setIsPlaying(false);
  }

  function handleReset() {
    setIsPlaying(false);
    setCurrentStep(0);
    if (actionsList.length) {
      setBoard(actionsList[0].board);
    }
  }

  // drive playback with effect
  useEffect(() => {
    if (isPlaying && actionsList.length) {
      // clear if any
      clearInterval(intervalRef.current);
      intervalRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          const next = Math.min(prev + 1, actionsList.length - 1);
          setBoard(actionsList[next].board);
          if (next >= actionsList.length - 1) {
            // stop when reaching end
            clearInterval(intervalRef.current);
            setIsPlaying(false);
          }
          return next;
        });
      }, speed);
    } else {
      // stopped or paused
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [isPlaying, speed, actionsList]);

  // adjust board when currentStep changes (e.g., user may click into steps later)
  useEffect(() => {
    if (actionsList.length && actionsList[currentStep]) {
      setBoard(actionsList[currentStep].board);
    }
  }, [currentStep, actionsList]);

  // update board when input changes
  useEffect(() => {
    const parsed = parseInitialState(initialInput);
    if (parsed.ok) {
      setBoard(parsed.state);
    }
  }, [initialInput]);

  // render
  return (
    <div className="min-h-screen bg-background p-4 sm:p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="text-center">
          <h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-2">
            🧩 Puzzle Solver AI
          </h1>
          <p className="text-sm text-muted-foreground">
            Solve 8-puzzle using advanced search algorithms • Fase 2
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                ⚙️ Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block text-foreground">Algorithm</label>
                <Select value={algorithm} onValueChange={(v) => setAlgorithm(v)}>
                  <SelectTrigger id="algorithm">
                    <SelectValue placeholder="Select algorithm" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="astar">A* Search</SelectItem>
                    <SelectItem value="bfs">Breadth-First Search</SelectItem>
                    <SelectItem value="dfs">Depth-First Search</SelectItem>
                    <SelectItem value="greedy">Greedy Best-First</SelectItem>
                    <SelectItem value="ucs">Uniform Cost</SelectItem>
                    <SelectItem value="ida">IDA*</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block text-foreground">Heuristic</label>
                <Select 
                  value={heuristic} 
                  onValueChange={(v) => setHeuristic(v)}
                  disabled={!["greedy", "astar", "ida"].includes(algorithm)}
                >
                  <SelectTrigger id="heuristic">
                    <SelectValue placeholder="Select heuristic" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="manhattan">Manhattan Distance</SelectItem>
                    <SelectItem value="misplaced">Misplaced Tiles</SelectItem>
                  </SelectContent>
                </Select>
                {!["greedy", "astar", "ida"].includes(algorithm) && (
                  <p className="text-xs text-muted-foreground mt-1">
                    Heuristic not used for this algorithm
                  </p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block text-foreground">Preset States</label>
                <Select onValueChange={handlePresetChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Load preset..." />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="solved">✅ Solved State</SelectItem>
                    <SelectItem value="easy">🟢 Easy (1-2 moves)</SelectItem>
                    <SelectItem value="medium">🟡 Medium (3-5 moves)</SelectItem>
                    <SelectItem value="hard">🔴 Hard (10+ moves)</SelectItem>
                    <SelectItem value="expert">⚫ Expert (20+ moves)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block text-foreground">Initial State</label>
                <Textarea
                  id="initial-input"
                  value={initialInput}
                  onChange={(e) => setInitialInput(e.target.value)}
                  placeholder={"1 2 3\n4 5 6\n7 0 8"}
                  className="font-mono text-sm"
                  rows={3}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Enter 9 numbers (0-8), use 0 for empty space
                </p>
              </div>

              {error && (
                <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                  <p className="text-destructive text-sm">{error}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-3">
                <Button 
                  id="solve-btn" 
                  onClick={() => handleSolve({ showStepByStep: false })} 
                  disabled={isSolving} 
                  className="w-full"
                >
                  {isSolving ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Solving...
                    </>
                  ) : (
                    "⚡ Solve Now"
                  )}
                </Button>
                <Button 
                  id="show-btn" 
                  variant="secondary" 
                  onClick={() => handleSolve({ showStepByStep: true })} 
                  disabled={isSolving} 
                  className="w-full"
                >
                  {isSolving ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Solving...
                    </>
                  ) : (
                    "🎬 Show Steps"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Board + metrics */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                🎯 Puzzle Board
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center space-y-6">
                <Board board={board} />

                {/* Metrics */}
                <div id="metrics" className="grid grid-cols-3 gap-4 w-full max-w-xl">
                  <div className="metrics-card text-center">
                    <div className="text-2xl sm:text-3xl font-bold text-primary mb-1">
                      {metrics.moves}
                    </div>
                    <div className="text-xs text-muted-foreground">Moves</div>
                  </div>
                  <div className="metrics-card text-center">
                    <div className="text-2xl sm:text-3xl font-bold text-secondary mb-1">
                      {Math.round(metrics.time)}ms
                    </div>
                    <div className="text-xs text-muted-foreground">Time</div>
                  </div>
                  <div className="metrics-card text-center">
                    <div className="text-2xl sm:text-3xl font-bold text-accent mb-1">
                      {metrics.nodes_explored}
                    </div>
                    <div className="text-xs text-muted-foreground">Nodes</div>
                  </div>
                </div>

                {/* Playback controls */}
                {actionsList.length > 0 && (
                  <div className="flex items-center flex-wrap gap-3 p-4 bg-muted/50 rounded-lg">
                    <Button 
                      id="play-btn" 
                      onClick={handlePlay} 
                      disabled={isPlaying || currentStep >= actionsList.length - 1} 
                      size="sm"
                      variant="outline"
                    >
                      <Play className="w-4 h-4" />
                    </Button>
                    <Button 
                      id="pause-btn" 
                      onClick={handlePause} 
                      disabled={!isPlaying} 
                      size="sm"
                      variant="outline"
                    >
                      <Pause className="w-4 h-4" />
                    </Button>
                    <Button 
                      onClick={handleReset} 
                      size="sm"
                      variant="outline"
                    >
                      <RotateCcw className="w-4 h-4" />
                    </Button>

                    <div className="flex items-center space-x-2 ml-4">
                      <span className="text-sm text-muted-foreground">Speed</span>
                      <div className="w-32">
                        <Slider 
                          min={100} 
                          max={2000} 
                          step={100} 
                          value={[speed]} 
                          onValueChange={(v) => setSpeed(v[0])}
                          className="cursor-pointer"
                        />
                      </div>
                      <span className="text-xs text-muted-foreground w-12">
                        {speed}ms
                      </span>
                    </div>

                    <div className="text-sm text-muted-foreground ml-auto">
                      Step {currentStep + 1} of {actionsList.length}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Actions List */}
        {actionsList.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                📋 Solution Steps
                <span className="text-sm font-normal text-muted-foreground">
                  ({actionsList.length} steps)
                </span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div id="actions-list" className="max-h-48 overflow-y-auto space-y-2">
                {actionsList.map((step, index) => (
                  <div
                    key={index}
                    onClick={() => setCurrentStep(index)}
                    className={`step-item flex justify-between items-center ${
                      index === currentStep ? "active" : ""
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-xs bg-background px-2 py-1 rounded border">
                        {index.toString().padStart(2, '0')}
                      </span>
                      <span className="font-medium">
                        {step.move}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-muted-foreground">
                      {step.heuristic !== null && step.heuristic !== undefined && (
                        <span>h={step.heuristic.toFixed(1)}</span>
                      )}
                      <span>d={step.depth}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Footer */}
        <footer className="text-center text-xs text-muted-foreground border-t pt-4">
          <p>
            🚀 Fase 2 - Web Interface • Built with Next.js + Tailwind CSS + Python FastAPI
          </p>
          <p className="mt-1">
            Make sure the Python API is running on <code>localhost:8000</code>
          </p>
        </footer>
      </div>
    </div>
  );
}
