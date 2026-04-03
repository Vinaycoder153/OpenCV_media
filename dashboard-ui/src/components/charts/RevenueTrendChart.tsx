import { ResponsiveContainer, Area, AreaChart, CartesianGrid, Tooltip, XAxis, YAxis } from 'recharts';
import type { TrendPoint } from '@/types';

export function RevenueTrendChart({ data }: { data: TrendPoint[] }) {
  return (
    <div className="h-[320px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 12, left: -14, bottom: 0 }}>
          <defs>
            <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#5D8CFF" stopOpacity={0.45} />
              <stop offset="95%" stopColor="#5D8CFF" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(148,163,184,0.18)" vertical={false} />
          <XAxis dataKey="label" tickLine={false} axisLine={false} stroke="rgba(148,163,184,0.72)" />
          <YAxis tickLine={false} axisLine={false} stroke="rgba(148,163,184,0.72)" tickFormatter={(value) => `₹${Math.round(Number(value) / 1000)}k`} />
          <Tooltip
            contentStyle={{
              background: 'rgba(10, 15, 30, 0.96)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '16px',
              color: '#fff',
            }}
            formatter={(value) => [`₹${Number(value).toLocaleString('en-IN')}`, 'Revenue']}
          />
          <Area type="monotone" dataKey="revenue" stroke="#5D8CFF" strokeWidth={3} fill="url(#revenueGradient)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
