module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:prettier/recommended',
    'plugin:react/recommended',
    'plugin:prettier/recommended', // Habilita Prettier como plugin
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react', 'prettier'],
  rules: {
    'no-unused-vars': 'warn', // Advertencia para variables no usadas
    'no-await-in-loop': 'warn', // Advertencia para await en bucles
    'no-console': 'off', // Permite console.log
    'prettier/prettier': 'error', // Muestra errores si el código no sigue las reglas de Prettier
  },
};
