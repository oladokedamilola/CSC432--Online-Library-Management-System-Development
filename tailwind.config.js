/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'form-gradient':
          'linear-gradient(180deg, #B5EBFD 0%, #6C8C97 100%)',
      },
    },
  },
  plugins: [],
};
