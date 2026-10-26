import type {Page} from '@playwright/test';
export async function openFilters(page:Page){if(await page.locator('#filters-panel').isHidden())await page.locator('#filters-button').click();}
export async function closeTools(page:Page){for(const panel of ['filters','layers'])if(await page.locator(`#${panel}-panel`).isVisible())await page.locator(`#close-${panel}`).click();}
export async function selectFilter(page:Page,id:string,value:string){await openFilters(page);await page.locator(id).selectOption(value);}
