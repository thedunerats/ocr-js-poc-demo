# OCR Client - React App

A modern React application for training and testing an OCR neural network with a drawing interface.

## Features

- 🎨 **Interactive Drawing Canvas**: Draw digits with your mouse
- 🎓 **Training Mode**: Collect and send training batches to the neural network
- 🧪 **Testing Mode**: Test predictions in real-time
- 🎯 **Batch Processing**: Automatically sends training data in batches of 10
- 📊 **Visual Feedback**: See training progress and prediction results
- 🎭 **Modern UI**: Beautiful gradient design with smooth animations

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- OCR server running on `http://localhost:3000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Usage

1. **Draw a Digit**: Click and drag on the canvas to draw a digit (0-9)
2. **Train**: 
   - Enter the digit you drew in the input field
   - Click "Train" to add it to the training batch
   - After 10 samples, the batch is automatically sent to the server
3. **Test**: Draw a digit and click "Test" to see what the network predicts
4. **Reset**: Clear the canvas to start over

## API Integration

The client connects to the Flask backend through a Vite proxy:

- **Development**: `http://localhost:5173/api` → `http://localhost:3000`
- **Production**: Configure your backend URL in `vite.config.js`

### API Endpoints

**POST /api**

Training request:
```json
{
  "train": true,
  "trainArray": [
    {"y0": [/* 400 pixel array */], "label": 5}
  ]
}
```

Prediction request:
```json
{
  "predict": true,
  "image": [/* 400 pixel array */]
}
```

## Project Structure

```
client/
├── src/
│   ├── components/
│   │   ├── DrawingCanvas.jsx      # Main canvas component
│   │   └── DrawingCanvas.css      # Canvas styles
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # App styles
│   ├── main.jsx                   # React entry point
│   └── index.css                  # Global styles
├── index.html                     # HTML template
├── vite.config.js                 # Vite configuration
└── package.json                   # Dependencies
```

## Configuration

### Change Backend URL

Edit `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:3000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

### Change Batch Size

Edit `DrawingCanvas.jsx`:

```javascript
const BATCH_SIZE = 10 // Change this value
```

## Technologies

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Canvas API**: Drawing interface
- **Fetch API**: HTTP requests to backend

## Development

- Hot Module Replacement (HMR) for instant updates
- ESLint for code quality
- Modern ES6+ JavaScript
- CSS with animations and responsive design

## Tips

- Train multiple variations of each digit for better accuracy
- Use different writing styles and sizes
- The more training data, the better the predictions
- The network requires at least 10 samples before training
