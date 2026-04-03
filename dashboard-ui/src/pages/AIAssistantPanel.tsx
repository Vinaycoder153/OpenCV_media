import { FormEvent, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, SendHorizonal } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import type { AssistantMessage } from '@/types';

interface AIAssistantPanelProps {
  messages: AssistantMessage[];
  loading: boolean;
  onSend: (problem: string) => Promise<void>;
}

export function AIAssistantPanel({ messages, loading, onSend }: AIAssistantPanelProps) {
  const [problem, setProblem] = useState('');

  const ordered = useMemo(() => [...messages], [messages]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const value = problem.trim();
    if (!value || loading) {
      return;
    }
    setProblem('');
    await onSend(value);
  };

  return (
    <div className="space-y-5">
      <Card className="surface-gradient">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" />
            AI Assistant Panel
          </CardTitle>
          <CardDescription>Ask strategic questions and get structured growth guidance.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-3">
            <Textarea
              value={problem}
              onChange={(event) => setProblem(event.target.value)}
              placeholder="Describe your business challenge. Example: Revenue is flat despite strong engagement. What should I do next?"
              className="min-h-[140px]"
            />
            <div className="flex items-center justify-between gap-3">
              <p className="text-xs text-muted-foreground">AI returns concise, action-ready output optimized for business operators.</p>
              <Button type="submit" disabled={loading || !problem.trim()}>
                {loading ? 'Thinking...' : 'Get AI Strategy'}
                <SendHorizonal className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <div className="space-y-3">
        {ordered.map((message, index) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.04 }}
            className={`rounded-[1.25rem] border p-4 ${
              message.role === 'assistant'
                ? 'border-primary/30 bg-primary/10'
                : 'border-white/10 bg-white/5'
            }`}
          >
            <div className="flex items-center justify-between gap-2">
              <Badge variant={message.role === 'assistant' ? 'success' : 'outline'}>{message.role === 'assistant' ? 'AI assistant' : 'You'}</Badge>
              <span className="text-xs text-muted-foreground">{message.timestamp}</span>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-foreground">{message.content}</p>
            {message.bullets?.length ? (
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {message.bullets.map((bullet) => (
                  <li key={bullet} className="flex gap-2">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary" />
                    <span>{bullet}</span>
                  </li>
                ))}
              </ul>
            ) : null}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
