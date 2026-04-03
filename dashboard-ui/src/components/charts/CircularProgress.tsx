export function CircularProgress({ value, label }: { value: number; label: string }) {
  const size = 136;
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center rounded-[1.5rem] border border-white/10 bg-white/5 p-5 text-center">
      <div className="relative h-[136px] w-[136px]">
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={radius} stroke="rgba(148,163,184,0.18)" strokeWidth={strokeWidth} fill="none" />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="url(#progressGradient)"
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
          />
          <defs>
            <linearGradient id="progressGradient" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#5D8CFF" />
              <stop offset="100%" stopColor="#66E3FF" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-3xl font-extrabold">{value}%</div>
          <div className="text-xs uppercase tracking-[0.24em] text-muted-foreground">score</div>
        </div>
      </div>
      <p className="mt-3 text-sm font-semibold text-foreground">{label}</p>
    </div>
  );
}
