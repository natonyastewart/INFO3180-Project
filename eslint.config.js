import antfu from '@antfu/eslint-config';
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default antfu(
	{
		vue: true,
		typescript: true,

		// Configuration preferences
		lessOpinionated: true,
		isInEditor: false,

		// Code style
		stylistic: {
			semi: true,
			indent: 'tab',
		},

		// Format settings
		formatters: true,

		ignores: [
			'node_modules',
			'**/node_modules',
		],
	},
	// --- Accessibility Rules ---
	jsxA11y.flatConfigs.recommended,
	// --- Custom Rule Overrides ---
	{
		rules: {
			'antfu/no-top-level-await': 'off', // Allow top-level await
			'style/brace-style': ['error', '1tbs'], // Use the default brace style
			'ts/consistent-type-definitions': 'off', // Use `type` instead of `interface`
			'node/prefer-global/process': 'off', // Allow using `process.env`
			'antfu/curly': 'off',
			'curly': 'off',
			'no-console': 'off',
			'no-case-declarations': 'off',
			'no-use-before-define': 'warn',
			'ts/no-use-before-define': 'warn',
			'unused-imports/no-unused-vars': 'warn',
		},
	},
);
