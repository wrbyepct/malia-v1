/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{html,js,tsx}"],
  theme: {
    extend: {
      width: {
        'chat-window': '700px'
      },
      maxHeight: {
        'title': '230px',
      },
      maxWidth: {
        '700': '700px',
      },
      minWidth: {
        '400': '400px',
        '500': '500px',  // min-w-250 utility for min-width: 250px
        '1/4': '25%',   // min-w-1/4 utility for min-width: 25%
        // ... add more custom values as needed
      },
      colors: {
        'lightblue-50': 'rgba(173, 216, 230, 0.5)',
        'transparent-purple': 'rgba(136, 11, 146, 0.20)',
        'cool-dark': "rgba(5, 15, 29, 0.84)",
        'cool-dark-light': "rgba(5, 15, 29, 0.34)",
        accent: {
          1: "hsl(var(--color-accent1) / <alpha-value>)",
          2: "hsl(var(--color-accent2) / <alpha-value>)",
        },
        bkg: "hsl(var(--color-bkg) / <alpha-value>)",
        content: "hsl(var(--color-content) / <alpha-value>)",
      },
      animation: {
        'pulse-scale': 'pulseScale 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'blob': 'Blob 7s infinite',
        'pink-blob': 'BlobPink 7s infinite'
      }
    },
  },
  plugins: [],
}

