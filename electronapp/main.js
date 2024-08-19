const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    console.log("window created")
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'renderer.js'),
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
}


console.log("test")
app.whenReady().then(createWindow);