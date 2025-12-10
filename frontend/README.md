# MenuSnap Home (React + Tailwind)

A mobile-first homepage for **MenuSnap**. Users can pick a menu photo (Gallery / Camera), try a demo, open settings, and view recent menus.  
No icon libraries are used—simple, accessible UI with Tailwind CSS.

---

## 1) Requirements
- **Node.js** 18+ (20+ recommended)
- **npm** (bundled with Node)

---

## 2) Install & Run

```bash
# install dependencies
npm install

# start dev server
npm run dev
```

Open the URL printed in the terminal (usually `http://localhost:5173`).

### Build & Preview

```bash
npm run build
npm run preview
```

---

## 3) Tech Stack
- **Vite + React 19**
- **Tailwind CSS v4** (via PostCSS plugin)
- Simple components: `MenuSnapHome`, `ActionButton`, `PillButton`

---

## 4) Project Structure

```
menusnaphome/
├─ public/
├─ src/
│  ├─ components/
│  │  ├─ ActionButton.jsx        # Square action card (title + subtitle)
│  │  └─ MenuSnapHome.jsx        # Home screen layout
│  ├─ App.jsx                    # Renders <MenuSnapHome />
│  ├─ index.css                  # Tailwind entry + tiny globals
│  └─ main.jsx                   # React root
├─ index.html
├─ postcss.config.js             # Tailwind v4 PostCSS plugin config
├─ vite.config.js
└─ package.json
```

---

## 5) Tailwind v4 Setup (already included)

If you start from a fresh Vite React app, ensure these files match:

**Install packages**
```bash
npm i react react-dom
npm i -D vite @tailwindcss/postcss postcss autoprefixer
```

**postcss.config.js**
```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
    autoprefixer: {},
  },
};
```

**src/index.css**
```css
@import "tailwindcss";

html, body, #root { height: 100%; }
```

**src/main.jsx**
```jsx
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(<App />);
```

**src/App.jsx**
```jsx
import MenuSnapHome from "./components/MenuSnapHome.jsx";
export default function App() { return <MenuSnapHome />; }
```

---

## 6) Scripts

- `npm run dev` — start the dev server
- `npm run build` — production build to `dist/`
- `npm run preview` — preview the production build locally

---

## 7) Troubleshooting

- **Tailwind classes not applied**  
  Ensure `postcss.config.js` uses `@tailwindcss/postcss` (Tailwind v4). Restart the dev server after changes.

- **Import warnings in VSCode/ESLint**  
  Include the `.jsx` extension in component imports, e.g.:
  ```jsx
  import MenuSnapHome from "./components/MenuSnapHome.jsx";
  ```

