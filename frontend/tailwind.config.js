module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        galaxy: {
          900: '#0a0026', // deep space
          800: '#1a0536',
          700: '#2d0a4d',
          600: '#3e1a6d',
          500: '#5f27b7', // purple
          400: '#3b82f6', // blue
          300: '#a5b4fc', // soft blue
          200: '#f5f3ff', // light
        },
        accent: '#ffe600', // yellow for GT logo
      },
      fontFamily: {
        galaxy: ['Orbitron', 'Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}; 