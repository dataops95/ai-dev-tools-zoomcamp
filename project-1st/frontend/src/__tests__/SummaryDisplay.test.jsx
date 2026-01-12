import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import SummaryDisplay from '../components/SummaryDisplay';

describe('SummaryDisplay', () => {
  const mockResult = {
    video_title: 'Test Video',
    duration: '10:30',
    summary: 'This is a test summary of the video content.',
    chapters: [
      {
        timestamp: '00:00:00',
        title: 'Introduction',
        description: 'Introduction to the topic'
      },
      {
        timestamp: '00:05:30',
        title: 'Main Content',
        description: 'Detailed discussion of the main topic'
      }
    ]
  };

  it('renders video information', () => {
    render(<SummaryDisplay result={mockResult} />);
    
    expect(screen.getByText('Results')).toBeInTheDocument();
    expect(screen.getByText('Test Video')).toBeInTheDocument();
    expect(screen.getByText('10:30')).toBeInTheDocument();
  });

  it('renders summary section', () => {
    render(<SummaryDisplay result={mockResult} />);
    
    expect(screen.getByText('Summary')).toBeInTheDocument();
    expect(screen.getByText('This is a test summary of the video content.')).toBeInTheDocument();
  });

  it('renders all chapters', () => {
    render(<SummaryDisplay result={mockResult} />);
    
    expect(screen.getByText('Chapters')).toBeInTheDocument();
    expect(screen.getByText('Introduction')).toBeInTheDocument();
    expect(screen.getByText('Introduction to the topic')).toBeInTheDocument();
    expect(screen.getByText('Main Content')).toBeInTheDocument();
    expect(screen.getByText('Detailed discussion of the main topic')).toBeInTheDocument();
  });

  it('displays chapter timestamps', () => {
    render(<SummaryDisplay result={mockResult} />);
    
    expect(screen.getByText('00:00:00')).toBeInTheDocument();
    expect(screen.getByText('00:05:30')).toBeInTheDocument();
  });

  it('renders copy buttons', () => {
    render(<SummaryDisplay result={mockResult} />);
    
    const copyButtons = screen.getAllByText('Copy');
    expect(copyButtons.length).toBeGreaterThan(0);
    expect(screen.getByText('Copy All')).toBeInTheDocument();
  });

  it('handles empty chapters array', () => {
    const resultWithNoChapters = {
      ...mockResult,
      chapters: []
    };
    
    render(<SummaryDisplay result={resultWithNoChapters} />);
    
    expect(screen.getByText('Chapters')).toBeInTheDocument();
    expect(screen.queryByText('Introduction')).not.toBeInTheDocument();
  });
});
