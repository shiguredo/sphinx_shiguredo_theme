import commonjs from "@rollup/plugin-commonjs";
import copy from "rollup-plugin-copy";
import typescript from "rollup-plugin-typescript2";

export default [
  {
    input: "./src/typescript/navi.ts",
    plugins: [
      typescript({
        tsconfig: "./tsconfig.json"
      }),
      commonjs(),
      copy({
        targets: [
          {
            src: [
              "./node_modules/bootstrap/dist/js/bootstrap.min.js.map",
              "./node_modules/bootstrap/dist/js/bootstrap.min.js",
            ],
            dest: "../sphinx_shiguredo_theme/static/js/",
          },
        ]
      }),
    ],
    output: {
      sourcemap: false,
      file: "../sphinx_shiguredo_theme/static/js/navi.js",
      format: "es",
    }
  },
];
