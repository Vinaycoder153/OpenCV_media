import { FormEvent, useState } from 'react';
import { Copy, RefreshCw, Sparkles } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import type { ContentResult } from '@/types';

interface SocialContentGeneratorProps {
  contentResult: ContentResult;
  loading: boolean;
  onGenerate: (input: { businessType: string; audience: string; tone: string }) => Promise<void>;
  onCopy: (value: string, label: string) => Promise<void>;
}

export function SocialContentGenerator({ contentResult, loading, onGenerate, onCopy }: SocialContentGeneratorProps) {
  const [businessType, setBusinessType] = useState('Cafe');
  const [audience, setAudience] = useState('Young professionals');
  const [tone, setTone] = useState('premium');

  const handleGenerate = async (event: FormEvent) => {
    event.preventDefault();
    await onGenerate({ businessType, audience, tone });
  };

  return (
    <div className="space-y-5">
      <Card className="surface-gradient">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Social Content Generator
          </CardTitle>
          <CardDescription>Generate publish-ready post copy, captions, hashtags, and reel concepts in one pass.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleGenerate} className="grid grid-cols-1 gap-3 md:grid-cols-4">
            <Input value={businessType} onChange={(e) => setBusinessType(e.target.value)} placeholder="Business type" />
            <Input value={audience} onChange={(e) => setAudience(e.target.value)} placeholder="Audience" />
            <Input value={tone} onChange={(e) => setTone(e.target.value)} placeholder="Tone" />
            <Button type="submit" disabled={loading}>
              {loading ? 'Generating...' : 'Regenerate'}
              <RefreshCw className="h-4 w-4" />
            </Button>
          </form>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Post</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground">{contentResult.post}</p>
            <Button variant="secondary" onClick={() => onCopy(contentResult.post, 'Post')}>
              <Copy className="h-4 w-4" />
              Copy Post
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Caption</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground">{contentResult.caption}</p>
            <Button variant="secondary" onClick={() => onCopy(contentResult.caption, 'Caption')}>
              <Copy className="h-4 w-4" />
              Copy Caption
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Hashtags</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex flex-wrap gap-2">
            {contentResult.hashtags.map((tag) => (
              <Badge key={tag} variant="outline" className="text-sm">
                {tag}
              </Badge>
            ))}
          </div>
          <Button variant="secondary" onClick={() => onCopy(contentResult.hashtags.join(' '), 'Hashtags')}>
            <Copy className="h-4 w-4" />
            Copy Hashtags
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Reel Idea</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm text-muted-foreground">{contentResult.reelIdea}</p>
          <Button variant="secondary" onClick={() => onCopy(contentResult.reelIdea, 'Reel idea')}>
            <Copy className="h-4 w-4" />
            Copy Reel Idea
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
