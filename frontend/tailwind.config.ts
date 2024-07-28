import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        brown: {
          50: '#f7f2ee',  // Very light brown
          100: '#ede0d4', // Lighter brown
          200: '#e1c5a5', // Light brown
          300: '#d3aa76', // Warm brown
          400: '#bf8c4a', // Medium brown
          500: '#a47033', // Standard brown
          600: '#865a26', // Darker brown
          700: '#683f1e', // Dark brown
          800: '#4b2c15', // Very dark brown
          900: '#321d0f', // Deepest brown
        }
      }
    },
  },

  plugins: [],
};
export default config;
