import DifficultyPicker from "@/components/ui/difficulty-picker";
import usePomodoro from "@/hooks/pomodoro";
import { useEffect, useState } from "react";
import "/public/css/focus.css";

export default function Pomodoro() {
  const { timer, stopTimer, countdown, round, isRunning, currentModeTime } =
    usePomodoro();

  const [progressLeft, setProgress] = useState(0);

  useEffect(() => {
    if (timer === 0) setProgress(0);
    setProgress((timer / currentModeTime) * 100);
  }, [timer, currentModeTime]);

  return (
    <div className="w-full h-full flex flex-col px-10 py-10 mx-auto max-w-3xl">
      {/* Header */}
      <div className="flex justify-between items-start mb-20 animate-fade-up">
        <div>
          <h1 className="font-heading text-4xl text-foreground/95 tracking-tight">
            Focus <span className="italic text-copper">Session</span>
          </h1>
          <p className="text-muted-foreground mt-1.5 text-sm">
            Deep work. No distractions.
          </p>
        </div>
        <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-md bg-card ring-1 ring-border/60">
          <div
            className={`w-1.5 h-1.5 rounded-full ${isRunning ? "bg-sage animate-pulse" : "bg-muted-foreground/30"}`}
          />
          <span className="text-[10px] font-mono font-medium text-muted-foreground uppercase tracking-wider">
            Round {round % 4 === 0 && round > 0 ? 4 : round % 4}/4
          </span>
        </div>
      </div>

      {/* Difficulty (hidden placeholder) */}
      <div className="mb-4 hidden opacity-50 hover:opacity-100 transition-opacity">
        <DifficultyPicker />
      </div>

      {/* Clock */}
      <div
        className="flex-1 flex flex-col items-center justify-center -mt-12 animate-fade-up"
        style={{ animationDelay: "120ms" }}
      >
        <Clock timer={timer} progressLeft={progressLeft} />

        <div className="mt-14 flex flex-col items-center gap-4">
          {isRunning ? (
            <button
              onClick={stopTimer}
              className="px-8 py-3 rounded-lg bg-card ring-1 ring-border/60 text-foreground/80 font-medium text-sm transition-all hover:ring-border hover:bg-secondary cursor-pointer"
            >
              Stop Session
            </button>
          ) : (
            <button
              onClick={countdown}
              className="px-8 py-3 rounded-lg bg-copper text-copper-foreground font-medium text-sm transition-all hover:brightness-110 shadow-lg shadow-copper/10 cursor-pointer"
            >
              Start Focus
            </button>
          )}
        </div>
      </div>

      {/*<div className="mt-auto flex justify-end">
        <FocusFeatureDebugMenu debug={debug} />
      </div>*/}
    </div>
  );
}

function Clock({
  timer,
  progressLeft,
}: {
  timer: number;
  progressLeft: number;
}) {
  return (
    <div className="relative flex items-center justify-center">
      <svg
        className="w-72 h-72 rotate-[-90deg]"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 100 100"
      >
        {/* Background ring */}
        <circle
          cx="50"
          cy="50"
          r="44"
          fill="none"
          className="stroke-border/40"
          strokeWidth="1.5"
        />
        {/* Progress ring */}
        <circle
          cx="50"
          cy="50"
          r="44"
          fill="none"
          className="stroke-copper transition-all duration-1000 ease-linear"
          strokeWidth="2"
          style={{
            strokeDasharray: 276.46,
            strokeDashoffset: 276.46 - (276.46 * (100 - progressLeft)) / 100,
          }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-5xl font-light tracking-tight text-foreground/90">
          {Math.floor(timer / 60)
            .toString()
            .padStart(2, "0")}
          <span className="text-muted-foreground/30 mx-0.5">:</span>
          {(timer % 60).toString().padStart(2, "0")}
        </span>
        <span className="mt-3 text-[10px] font-mono text-muted-foreground/40 tracking-widest uppercase">
          {(100 - progressLeft).toFixed(0)}% remaining
        </span>
      </div>
    </div>
  );
}
