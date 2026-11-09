/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        whatsapp: {
          dark: '#075E54',
          teal: '#128C7E',
          green: '#25D366',
          light: '#DCF8C6',
          chatBg: '#EFEAE2',
          panel: '#F0F2F5',
          bubbleOut: '#D9FDD3',
          bubbleIn: '#FFFFFF',
          gray: '#667781',
          border: '#E9EDEF',
        }
      },
      backgroundImage: {
        'whatsapp-pattern': "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\" opacity=\"0.06\"><text x=\"20\" y=\"30\" font-size=\"20\">🎓</text><text x=\"120\" y=\"80\" font-size=\"20\">📚</text><text x=\"40\" y=\"140\" font-size=\"20\">📝</text><text x=\"150\" y=\"160\" font-size=\"20\">📊</text></svg>')",
      }
    },
  },
  plugins: [],
}

