const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 900 });
    await page.goto('file:///Users/user/git/systems-and-intelligence/docs/interactive/sii-dashboard-app.html');

    // Wait for charts to animate and render
    await new Promise(r => setTimeout(r, 2000));

    await page.screenshot({ path: '/Users/user/.gemini/antigravity/brain/87203fe9-1856-44a8-8859-4580293d16cf/sii_dashboard_interactive.png' });
    await browser.close();
})();
