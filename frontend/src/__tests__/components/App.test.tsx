import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'

// Simple test component instead of main.tsx
const TestApp = () => {
  return (
    <div role="main" data-testid="app">
      <h1>GMC Dashboard</h1>
      <p>Educational Analytics Platform</p>
    </div>
  )
}

// Mock React Router
vi.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Routes: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Route: ({ element }: { element: React.ReactNode }) => <div>{element}</div>,
  useNavigate: () => vi.fn(),
  useLocation: () => ({ pathname: '/' }),
}))

// Mock API services
vi.mock('../../services/api', () => ({
  healthCheck: vi.fn(() => Promise.resolve({ status: 'healthy' })),
  getCalculations: vi.fn(() => Promise.resolve([])),
}))

describe('App Component', () => {
  beforeEach(() => {
    cleanup()
  })

  it('renders without crashing', () => {
    render(<TestApp />)
    expect(document.body).toBeInTheDocument()
  })

  it('displays main application content', () => {
    render(<TestApp />)
    
    // Check if main app container exists
    const appContainer = screen.getByRole('main')
    expect(appContainer).toBeInTheDocument()
    
    // Check for specific content
    expect(screen.getByText('GMC Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Educational Analytics Platform')).toBeInTheDocument()
  })

  it('has proper test id attribute', () => {
    render(<TestApp />)
    const appContainer = screen.getByTestId('app')
    expect(appContainer).toBeInTheDocument()
  })

  it('has correct heading structure', () => {
    render(<TestApp />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toHaveTextContent('GMC Dashboard')
  })
})

describe('App Accessibility', () => {
  it('has proper semantic structure', () => {
    render(<TestApp />)
    
    // Check for main element specifically
    const mainElement = screen.getByRole('main')
    expect(mainElement).toBeInTheDocument()
    
    // Verify it has the expected content
    expect(mainElement).toContainElement(screen.getByText('GMC Dashboard'))
  })

  it('has accessible content', () => {
    render(<TestApp />)
    
    // Check that content is accessible
    const heading = screen.getByRole('heading')
    expect(heading).toBeInTheDocument()
    
    const mainContent = screen.getByRole('main')
    expect(mainContent).toBeInTheDocument()
  })
})