import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

// Placeholder App component - will be enhanced in future stories
function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          GMC Dashboard
        </h1>
        <p className="text-gray-600 mb-6">
          Educational Analytics Platform for Strategic Business Analysis
        </p>
        <div className="bg-blue-50 p-4 rounded-md">
          <p className="text-sm text-blue-800">
            Foundation setup complete. Frontend microservices integration coming in next stories.
          </p>
        </div>
      </div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)