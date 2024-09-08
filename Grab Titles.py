from playwright.async_api import async_playwright
import asyncio
import time
import itertools
import re


async def main(url):
    async with async_playwright() as playwright:

        browser = await playwright.firefox.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)

        time.sleep(1)

        website = re.match('.*?.com', url).group(0)

        for next_page in range(int(input('Input how many pages you want to search: '))):
            titles = await page.query_selector_all('.css-19uc56f')
            job_titles = [await title.inner_text() for title in titles]

            links = await page.query_selector_all('[data-automation-id="jobTitle"]')
            links_titles = [website + await link.get_attribute('href') for link in links]

            combined_titles = list(zip(job_titles, links_titles))
            finish_combined = list(itertools.chain(*combined_titles))

            n = 1
            n += int(next_page)
            print(f"Page #" + str(n))

            for separator in range(0, len(finish_combined)):
                print(finish_combined[separator])

            time.sleep(1)

            await page.locator('[data-uxi-element-id="next"]').click()

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main('https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite'))
