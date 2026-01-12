import { describe, it, expect, vi, beforeEach } from 'vitest';
import { processVideo, checkHealth } from '../services/api';

// Mock fetch
global.fetch = vi.fn();

describe('API Service', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('processVideo', () => {
    it('successfully processes a video', async () => {
      const mockResponse = {
        video_title: 'Test Video',
        duration: '10:00',
        summary: 'Test summary',
        chapters: []
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await processVideo(
        'https://www.youtube.com/watch?v=test',
        'test-api-key'
      );

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/videos/process'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: expect.stringContaining('youtube_url')
        })
      );
    });

    it('throws error on failed request', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Invalid URL' })
      });

      await expect(
        processVideo('invalid-url', 'test-api-key')
      ).rejects.toThrow('Invalid URL');
    });

    it('throws generic error when detail is missing', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({})
      });

      await expect(
        processVideo('test-url', 'test-api-key')
      ).rejects.toThrow('Failed to process video');
    });
  });

  describe('checkHealth', () => {
    it('successfully checks health', async () => {
      const mockHealth = {
        status: 'healthy',
        service: 'YouTube Video Summarizer API'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHealth
      });

      const result = await checkHealth();

      expect(result).toEqual(mockHealth);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/health')
      );
    });

    it('throws error on failed health check', async () => {
      fetch.mockResolvedValueOnce({
        ok: false
      });

      await expect(checkHealth()).rejects.toThrow('API health check failed');
    });
  });
});
