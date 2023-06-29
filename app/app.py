from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()


@app.get("/")
async def scrape_website():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        await browser.close()
        return {"title": title}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)