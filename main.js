const { app, BrowserWindow, Menu, ipcMain, nativeTheme } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');

  // Automatically switch theme
  nativeTheme.on('updated', () => {
    win.webContents.send('theme-updated', nativeTheme.shouldUseDarkColors ? 'dark' : 'light');
  });
}

app.whenReady().then(() => {
  createWindow();

  const isMac = process.platform === 'darwin';
  const template = [
    // File menu
    {
      label: 'File',
      submenu: [
        { label: 'New...', accelerator: 'CmdOrCtrl+N' },
        { label: 'Save', accelerator: 'CmdOrCtrl+S' },
        { type: 'separator' },
        { label: 'Exit', accelerator: 'CmdOrCtrl+Q', role: isMac ? 'close' : 'quit' }
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
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
