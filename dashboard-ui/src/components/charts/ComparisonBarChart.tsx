import { ResponsiveContainer, BarChart, Bar, CartesianGrid, Tooltip, XAxis, YAxis } from 'recharts';
import type { ComparisonPoint } from '@/types';

export function ComparisonBarChart({ data }: { data: ComparisonPoint[] }) {
  return (
    <div className="h-[320px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 12, left: -18, bottom: 0 }}>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(148,163,184,0.18)" vertical={false} />
          <XAxis dataKey="label" tickLine={false} axisLine={false} stroke="rgba(148,163,184,0.72)" />
          <YAxis tickLine={false} axisLine={false} stroke="rgba(148,163,184,0.72)" />
          <Tooltip
            contentStyle={{
              background: 'rgba(10, 15, 30, 0.96)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '16px',
              color: '#fff',
            }}
          />
          <Bar dataKey="value" radius={[14, 14, 0, 0]} fill="#66E3FF" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
