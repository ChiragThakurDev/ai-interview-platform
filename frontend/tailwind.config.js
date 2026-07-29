/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // LeetCode-inspired orange accent
        brand: {
          50:  '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f89f1b',  // LeetCode orange
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },
        // Dark neutrals — LeetCode-like dark surface
        neutral: {
          0:    '#ffffff',
          50:   '#f9fafb',
          100:  '#f3f4f6',
          150:  '#ebebeb',
          200:  '#e5e7eb',
          300:  '#d1d5db',
          400:  '#9ca3af',
          500:  '#6b7280',
          600:  '#4b5563',
          700:  '#374151',
          800:  '#1f2937',
          850:  '#1a1f2e',
          900:  '#111827',
          925:  '#0d111a',
          950:  '#0a0e17',
        },
        // Code-editor dark surfaces
        surface: {
          base:    '#1a1a1a',   // main bg
          card:    '#282828',   // card bg
          raised:  '#333333',   // elevated
          border:  '#3d3d3d',   // border
          hover:   '#3a3a3a',   // hover bg
          muted:   '#404040',   // subtle
        },
        // Light mode surfaces
        lsurface: {
          base:    '#f9fafb',
          card:    '#ffffff',
          raised:  '#f3f4f6',
          border:  '#e5e7eb',
          hover:   '#f3f4f6',
        },
        // Semantic colors
        green:  { 400: '#4ade80', 500: '#22c55e', 600: '#16a34a' },
        yellow: { 400: '#facc15', 500: '#eab308', 600: '#ca8a04' },
        red:    { 400: '#f87171', 500: '#ef4444', 600: '#dc2626' },
        blue:   { 400: '#60a5fa', 500: '#3b82f6', 600: '#2563eb' },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
        xs:    ['0.75rem',  { lineHeight: '1rem' }],
        sm:    ['0.8125rem', { lineHeight: '1.25rem' }],
        base:  ['0.875rem', { lineHeight: '1.375rem' }],
        lg:    ['1rem',     { lineHeight: '1.5rem' }],
        xl:    ['1.125rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.25rem',  { lineHeight: '1.75rem' }],
        '3xl': ['1.5rem',   { lineHeight: '2rem' }],
      },
      boxShadow: {
        'sm':    '0 1px 2px 0 rgb(0 0 0 / 0.3)',
        'DEFAULT':'0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3)',
        'md':    '0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.2)',
        'lg':    '0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.2)',
        'xl':    '0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.2)',
        'orange': '0 0 0 2px rgba(248, 159, 27, 0.3)',
        'none':  'none',
      },
      borderRadius: {
        'none': '0',
        'sm':   '0.25rem',
        'DEFAULT':'0.375rem',
        'md':   '0.5rem',
        'lg':   '0.625rem',
        'xl':   '0.75rem',
        '2xl':  '1rem',
        'full': '9999px',
      },
      animation: {
        'fade-in':   'fadeIn 0.2s ease-out',
        'fade-up':   'fadeUp 0.25s ease-out',
        'slide-in':  'slideIn 0.25s ease-out',
        'spin-slow': 'spin 2s linear infinite',
        'pulse-dot': 'pulseDot 1.5s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%':   { opacity: '0', transform: 'translateX(-8px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0.4' },
        },
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
      },
    },
  },
  plugins: [],
}
