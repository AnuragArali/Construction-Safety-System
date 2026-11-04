/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0a0f1d',
          800: '#0f172a',
          700: '#1e293b',
          600: '#334155'
        },
        safety: {
          orange: '#f97316',
          amber: '#f59e0b',
          red: '#ef4444',
          green: '#10b981'
        }
      }
    },
  },
  plugins: [],
}
