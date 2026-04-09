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
  onGenerate: (input: { businessType: string; audience: string; tone: string; platform: string }) => Promise<void>;
  onCopy: (value: string, label: string) => Promise<void>;
}

const PLATFORMS = ['Instagram', 'Facebook', 'WhatsApp', 'Google Business', 'Reels'];

export function SocialContentGenerator({ contentResult, loading, onGenerate, onCopy }: SocialContentGeneratorProps) {
  const [businessType, setBusinessType] = useState('Cafe');
  const [audience, setAudience] = useState('Young professionals');
  const [tone, setTone] = useState('premium');
  const [platform, setPlatform] = useState('Instagram');

  const handleGenerate = async (event: FormEvent) => {
    event.preventDefault();
    await onGenerate({ businessType, audience, tone, platform });
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
        <CardContent className="space-y-4">
          {/* Platform selector */}
          <div>
            <p className="mb-2 text-xs text-muted-foreground">Platform</p>
            <div className="flex flex-wrap gap-2">
              {PLATFORMS.map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPlatform(p)}
                  className={`rounded-full border px-3 py-1.5 text-xs font-medium transition-all ${
                    platform === p
                      ? 'border-primary bg-primary/15 text-primary shadow-glow'
                      : 'border-white/10 bg-white/5 text-muted-foreground hover:border-white/20 hover:bg-white/10'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleGenerate} className="grid grid-cols-1 gap-3 md:grid-cols-4">
            <Input value={businessType} onChange={(e) => setBusinessType(e.target.value)} placeholder="Business type" />
            <Input value={audience} onChange={(e) => setAudience(e.target.value)} placeholder="Audience" />
            <Input value={tone} onChange={(e) => setTone(e.target.value)} placeholder="Tone (premium / fun / bold)" />
            <Button type="submit" disabled={loading}>
              {loading ? 'Generating...' : 'Generate'}
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </Button>
          </form>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Post Copy</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm leading-relaxed text-muted-foreground">{contentResult.post}</p>
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
            <p className="text-sm leading-relaxed text-muted-foreground">{contentResult.caption}</p>
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
              <Badge key={tag} variant="outline" className="cursor-pointer text-sm transition hover:bg-primary/15" onClick={() => onCopy(tag, 'Hashtag')}>
                {tag}
              </Badge>
            ))}
          </div>
          <Button variant="secondary" onClick={() => onCopy(contentResult.hashtags.join(' '), 'Hashtags')}>
            <Copy className="h-4 w-4" />
            Copy All Hashtags
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Reel Idea</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm leading-relaxed text-muted-foreground">{contentResult.reelIdea}</p>
          <Button variant="secondary" onClick={() => onCopy(contentResult.reelIdea, 'Reel idea')}>
            <Copy className="h-4 w-4" />
            Copy Reel Idea
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

interface SocialContentGeneratorProps {
  contentResult: ContentResult;
  loading: boolean;
  onGenerate: (input: { businessType: string; audience: string; tone: string }) => Promise<void>;
  onCopy: (value: string, label: string) => Promise<void>;
}
