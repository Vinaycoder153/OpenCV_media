import { useState } from 'react';
import { MessageSquareMore, SendHorizonal } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { ReviewItem } from '@/types';

interface ReviewAnalyzerProps {
  reviews: ReviewItem[];
  loading: boolean;
  onAnalyze: () => Promise<void>;
  onReplyPreview: (reply: string) => void;
}

const sentimentVariant: Record<ReviewItem['sentiment'], 'success' | 'warning' | 'danger'> = {
  positive: 'success',
  neutral: 'warning',
  negative: 'danger',
};

export function ReviewAnalyzer({ reviews, loading, onAnalyze, onReplyPreview }: ReviewAnalyzerProps) {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="space-y-5">
      <Card className="surface-gradient">
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MessageSquareMore className="h-5 w-5 text-primary" />
              Review Analyzer
            </CardTitle>
            <CardDescription>Classify sentiment and generate contextual AI replies.</CardDescription>
          </div>
          <Button onClick={onAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Reviews'}
          </Button>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {reviews.map((review) => (
          <Card
            key={review.id}
            className={selected === review.id ? 'border-primary/40' : undefined}
          >
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <CardTitle className="text-base">{review.author}</CardTitle>
                  <CardDescription>{review.location} · {review.rating}/5</CardDescription>
                </div>
                <Badge variant={sentimentVariant[review.sentiment]}>{review.sentiment}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-muted-foreground">{review.review}</p>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-3 text-sm text-foreground">
                <p className="mb-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">AI Reply</p>
                <p>{review.reply}</p>
              </div>
              <Button
                variant="secondary"
                onClick={() => {
                  setSelected(review.id);
                  onReplyPreview(review.reply);
                }}
              >
                <SendHorizonal className="h-4 w-4" />
                Use AI Reply
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
