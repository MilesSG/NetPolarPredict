/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#4B6BFB',
          DEFAULT: '#3659E3',
          dark: '#2A4DE0',
        },
        secondary: {
          light: '#FF7D51',
          DEFAULT: '#FF6B3D',
          dark: '#FF5A29',
        },
        dark: {
          light: '#2C3E50',
          DEFAULT: '#1E293B',
          dark: '#0F172A',
        },
      },
    },
  },
  plugins: [],
}

