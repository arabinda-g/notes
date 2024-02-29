const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    title: "Your Main Window Title", // Set the window title
    icon: path.join(__dirname, 'icon.png') // Set the window icon
  });

  mainWindow.loadFile('index.html');

  // Remove the menu from the main window
  // mainWindow.setMenu(null);
}

function createAddButtonWindow() {
  // Ensure mainWindow is already created
  if (!mainWindow) return;

  let addButtonWindow = new BrowserWindow({
    width: 400,
    height: 600,
    modal: true,
    parent: mainWindow,
    show: false, // Don't show until ready-to-show is emitted
    resizable: false, // Disable resizing
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  addButtonWindow.loadFile('addButton.html');
  addButtonWindow.removeMenu(); // Remove the menu from the popup window
  addButtonWindow.once('ready-to-show', () => addButtonWindow.show());

  // Handle window closed
  addButtonWindow.on('closed', () => addButtonWindow = null);
}

app.whenReady().then(createMainWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createMainWindow();
});

// Example menu setup with the new "New..." action
const isMac = process.platform === 'darwin';
const template = [
  {
    label: 'File',
    submenu: [
      {
        label: 'New...',
        accelerator: 'CmdOrCtrl+N',
        click: () => {
          createAddButtonWindow();
        }
      },
      { type: 'separator' },
      { role: isMac ? 'close' : 'quit' }
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
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
