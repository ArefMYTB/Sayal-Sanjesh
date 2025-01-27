import * as path from "path";

import { defineConfig, loadEnv } from "vite";

import { VitePWA } from "vite-plugin-pwa";
import { createHtmlPlugin } from "vite-plugin-html";
import manifest from "./manifest.json";

// import react from "`@vitejs/plugin-react`";

// import { join, resolve } from 'path';

// import transformPlugin from 'vite-plugin-transform';

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = Object.assign(process.env, loadEnv(mode, process.cwd(), ""));
  return defineConfig({
    esbuild: {
      pure: mode === "production" ? ["console", "debugger"] : [],
    },
    plugins: [
      VitePWA({
        manifest,
        includeAssets: [
          "favicon.svg",
          "favicon.ico",
          "robots.txt",
          "apple-touch-icon.png",
        ],
        // switch to "true" to enable sw on development
        devOptions: {
          enabled: false,
        },
        workbox: {
          globPatterns: ["**/*.{js,css,html}", "**/*.{svg,png,jpg,gif}"],
        },
      }),
      createHtmlPlugin({
        minify: true,
        entry: "/src/main.tsx",
        template: "index.html",
        inject: {
          data: {
            title: "index",
            injectScript: `<script src="./inject.js"></script>`,
          },
          tags: [
            {
              injectTo: "body-prepend",
              tag: "div",
              attrs: {
                id: "tag",
              },
            },
          ],
        },
      }),
      // transformPlugin({
      //   tStart: '%{',
      //   tEnd: '}%',
      //   replaceFiles: [resolve(join(__dirname, '/dist/manifest.json'))],
      //   replace: {
      //     VITE_ENGLISH_TITLE: process.env.VITE_ENGLISH_TITLE,
      //     VITE_TITLE: process.env.VITE_TITLE,
      //     VITE_DESCRIPTION: process.env.VITE_DESCRIPTION,
      //   },
      // }),
    ],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes("node_modules")) {
              return id
                .toString()
                .split("node_modules/")[1]
                .split("/")[0]
                .toString();
            }
          },
        },
      },
    },
  });
};
