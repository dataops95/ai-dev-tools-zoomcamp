import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import VideoInput from '../components/VideoInput';

describe('VideoInput', () => {
  it('renders the form with all fields', () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    expect(screen.getByText('YouTube Video Summarizer')).toBeInTheDocument();
    expect(screen.getByLabelText('YouTube URL')).toBeInTheDocument();
    expect(screen.getByLabelText('Gemini API Key')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Summarize Video/i })).toBeInTheDocument();
  });

  it('shows validation error for empty URL', async () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    const submitButton = screen.getByRole('button', { name: /Summarize Video/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('YouTube URL is required')).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('shows validation error for invalid URL', async () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    const urlInput = screen.getByLabelText('YouTube URL');
    const apiKeyInput = screen.getByLabelText('Gemini API Key');
    const submitButton = screen.getByRole('button', { name: /Summarize Video/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://invalid-url.com' } });
    fireEvent.change(apiKeyInput, { target: { value: 'test-key' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Please enter a valid YouTube URL')).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('accepts valid youtube.com URL', async () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    const urlInput = screen.getByLabelText('YouTube URL');
    const apiKeyInput = screen.getByLabelText('Gemini API Key');
    const submitButton = screen.getByRole('button', { name: /Summarize Video/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' } });
    fireEvent.change(apiKeyInput, { target: { value: 'test-api-key' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        youtubeUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        geminiApiKey: 'test-api-key'
      });
    });
  });

  it('accepts valid youtu.be URL', async () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    const urlInput = screen.getByLabelText('YouTube URL');
    const apiKeyInput = screen.getByLabelText('Gemini API Key');
    const submitButton = screen.getByRole('button', { name: /Summarize Video/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://youtu.be/dQw4w9WgXcQ' } });
    fireEvent.change(apiKeyInput, { target: { value: 'test-api-key' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        youtubeUrl: 'https://youtu.be/dQw4w9WgXcQ',
        geminiApiKey: 'test-api-key'
      });
    });
  });

  it('shows validation error for empty API key', async () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={false} />);
    
    const urlInput = screen.getByLabelText('YouTube URL');
    const submitButton = screen.getByRole('button', { name: /Summarize Video/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://www.youtube.com/watch?v=test' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Gemini API key is required')).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('disables form when loading', () => {
    const mockOnSubmit = vi.fn();
    render(<VideoInput onSubmit={mockOnSubmit} isLoading={true} />);
    
    const urlInput = screen.getByLabelText('YouTube URL');
    const apiKeyInput = screen.getByLabelText('Gemini API Key');
    const submitButton = screen.getByRole('button', { name: /Processing.../i });
    
    expect(urlInput).toBeDisabled();
    expect(apiKeyInput).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });
});
