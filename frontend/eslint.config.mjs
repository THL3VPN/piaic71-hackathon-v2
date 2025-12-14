import path from "node:path";
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import tsParser from "@typescript-eslint/parser";

export default [
  ...nextCoreWebVitals,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: path.resolve("./tsconfig.json"),
        tsconfigRootDir: path.resolve("./")
      }
    },
    rules: {
      "react/react-in-jsx-scope": "off"
    }
  }
];
