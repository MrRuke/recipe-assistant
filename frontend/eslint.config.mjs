import js from "@eslint/js";
import stylistic from '@stylistic/eslint-plugin';
import { defineConfig } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";

export default defineConfig([
    {
        ...stylistic.configs['recommended'],
        files: ["**/*.{js,mjs,cjs,ts,mts,cts}"],
        plugins: {
            js,
            '@stylistic': stylistic
        },
        extends: ["js/recommended"],
        languageOptions: { globals: globals.browser },
        rules: {
            '@stylistic/indent': ['error', 4],
            '@stylistic/semi': ['error', 'always'],
        }
    },
    tseslint.configs.recommended,
]);
