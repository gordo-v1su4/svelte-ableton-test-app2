# Svelte + Vite + Ableton Integration

A Svelte application for visualizing Ableton Live session data with waveform analysis.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pnpm install
   ```

2. **Run Development Server**
   ```bash
   pnpm run dev
   ```
   Then open [http://localhost:5173](http://localhost:5173) in your browser.

3. **Build for Production**
   ```bash
   pnpm run build
   pnpm run preview
   ```

## 🛠️ Project Structure

```
svelte-ableton-test-app/
├── public/                     # Static assets
│   ├── ableton_data_export.json  # JSON from Ableton API script
│   └── audio.wav                # Sample audio file
├── src/
│   ├── components/             # Svelte components
│   │   ├── SessionInfo.svelte   # Session metadata
│   │   ├── TransientList.svelte # Transient markers
│   │   └── WaveformViewer.svelte # Waveform visualization
│   ├── lib/                    # Utility functions
│   │   ├── data.js             # Data handling
│   │   └── time.js             # Time conversions
│   ├── App.svelte              # Root component
│   └── main.js                 # App entry point
└── package.json                # Project configuration
```

## 🔧 Requirements

- Node.js 16+
- pnpm 7+

## 📚 Technologies Used

- [Svelte](https://svelte.dev/)
- [Vite](https://vitejs.dev/)
- [Peaks.js](https://waveform.prototyping.bbc.co.uk/)

## 🔌 VS Code Setup

For the best development experience, install the [Svelte extension](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).