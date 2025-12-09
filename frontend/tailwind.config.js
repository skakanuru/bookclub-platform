/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2C5F4F',
          light: '#3A7860',
          dark: '#1F4538',
        },
        background: '#FAF9F6',
        surface: '#FFFFFF',
        border: '#E8E6E1',
        text: {
          primary: '#2B2B2B',
          secondary: '#6B6B6B',
          tertiary: '#9B9B9B',
        },
        accent: '#C7956D',
        danger: '#C85A54',
        success: '#5A8C6F',
      },
      fontFamily: {
        serif: ['Merriweather', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Courier', 'monospace'],
      },
      boxShadow: {
        'sm': '0 1px 3px rgba(0,0,0,0.08)',
        'md': '0 4px 12px rgba(0,0,0,0.1)',
        'lg': '0 8px 24px rgba(0,0,0,0.12)',
      },
    },
  },
  plugins: [],
}
