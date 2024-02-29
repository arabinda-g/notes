const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

function createWindow() {
  // Create the main window
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('index.html');
}

function createAddButtonWindow() {
  // Create the add button window
  let addButtonWindow = new BrowserWindow({
    width: 400,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // For simplicity, adjust according to your security needs
      enableRemoteModule: true // Depending on Electron version, might not be needed
    }
  });

  addButtonWindow.loadFile('addButton.html');
}

app.whenReady().then(() => {
  createWindow();

  const menu = Menu.buildFromTemplate([
    {
      label: 'File',
      submenu: [
        {
          label: 'New...',
          accelerator: 'Ctrl+N',
          click: () => {
            createAddButtonWindow();
          }
        },
        { label: 'Save', accelerator: 'Ctrl+S' },
        { type: 'separator' },
        { label: 'Exit', accelerator: 'Ctrl+Q', role: 'quit' }
      ]
    },
    // Edit menu
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: 'Redo', accelerator: 'CmdOrCtrl+Y', role: 'redo' },
        { type: 'separator' },
        { label: 'Movable', accelerator: 'CmdOrCtrl+D' }
      ]
    },

    // Devtools menu
    {
      label: 'Devtools',
      submenu: [
        {
          label: 'Toggle DevTools',
          accelerator: 'F12',
          click: (item, focusedWindow) => {
            focusedWindow.toggleDevTools();
          }
        },
        {
          role: 'reload'
        }
      ]
    }
  ]);

  Menu.setApplicationMenu(menu);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
