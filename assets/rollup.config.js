import commonjs from "@rollup/plugin-commonjs";
import typescript from "rollup-plugin-typescript2";

export default [
  {
    input: "./src/typescript/navi.ts",
    plugins: [
      typescript({
        tsconfig: "./tsconfig.json"
      }),
      commonjs(),
    ],
    output: {
      sourcemap: false,
      file: "../sphinx_shiguredo_theme/static/js/navi.js",
      format: "es",
    }
  },
];
