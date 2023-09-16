const { app, BrowserWindow } = require('electron')
const path = require('node:path')

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
        backgroundColor: '#00000000',
        icon: 'public/favicon.ico',
        show: false,
        
        minHeight: 500,
        minWidth: 800,

        titleBarStyle: 'hidden',
        titleBarOverlay: {
            color: '#00000000',
            symbolColor: '#ffffff',
            height: 38
        },

        height: 600,
        width: 940,

        webPreferences: {
            preload: path.join(__dirname, '/public/preload.js')
        }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('public/index.html')
  mainWindow.removeMenu();

  // Open the DevTools.
//   mainWindow.webContents.openDevTools()

  // Show the window only when loaded
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.