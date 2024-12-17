module.exports = {
  content: [
    "./templates/**/*.html",  // Add paths to your templates
    "./static/**/*.js",       // Add paths to your JS files if applicable
  ],
  theme: {
    extend: {
      colors: {
        'primary-bg-color': '#2C3E50',   // Light Grayish White for background
        'button-color':'#D8C4B6',
        'bg-color': '#2D3748',  // Dark Gray for text
        'primary-text-color': '#ECF0F1', // Teal for primary buttons
        'secondary-text-color': '#95A5A6', // Darker Teal for hover
        'secondary-btn': '#63B3DE', // Light Blue for secondary buttons
        'secondary-btn-hover':'#3275a8',
        'button-hover': '#F5EFE7' // Darker Blue for hover
      },
      fontFamily: {
        'roboto': ['Roboto', 'sans-serif'],
        'Quicksand': ['Quicksand', 'sans-serif'],
        'poppins': ['Poppins', 'sans-serif']
      },
    },
  },
  plugins: [],
}
