module.exports = {
  content: [
    "./templates/**/*.html",  // Add paths to your templates
    "./static/**/*.js",       // Add paths to your JS files if applicable
  ],
  theme: {
    extend: {
      colors: {
        'bg-color': '#F7FFFC',   // Light Grayish White for background
        'text-color': '#2D3748',  // Dark Gray for text
        'primary-btn': '#38B2AC', // Teal for primary buttons
        'primary-btn-hover': '#319795', // Darker Teal for hover
        'secondary-btn': '#63B3ED', // Light Blue for secondary buttons
        'secondary-btn-hover': '#3182CE' // Darker Blue for hover
      },
      fontFamily: {
        'roboto': ['Roboto', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
        'poppins': ['Poppins', 'sans-serif']
      },
    },
  },
  plugins: [],
}
