import asyncio
from playwright.async_api import async_playwright

class BrowserGym:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None

    async def start(self):
        """Starts the browser and goes to the Sandbox"""
        # headless=False means you SEE the browser. Set to True to hide it.
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        
        # Navigate to your React App
        try:
            await self.page.goto("http://localhost:3000")
        except Exception as e:
            print(f"Error connecting to frontend: {e}")
        
    async def get_state(self, success_text="Mission Complete"):
        """
        Returns the current state.
        :param success_text: The specific text we need to find to prove we won.
        """
        if not self.page:
            return {"error": "Browser not started"}
        
        try:
            title = await self.page.title()
            url = self.page.url
            
            # Playwright selector 'text=' finds any element containing that string
            success_element = await self.page.query_selector(f"text={success_text}")
            is_success = success_element is not None

            return {
                "title": title,
                "url": url,
                "done": is_success,
                "reward": 100 if is_success else 0
            }
        except Exception as e:
            return {"error": str(e), "reward": 0, "done": False}

    async def execute_action(self, action_type: str, selector: str, value: str = ""):
        """
        Executes an action: Click or Type
        """
        if not self.page:
            return {"status": "failed", "error": "Browser not initialized"}

        try:
            if action_type == "type":
                # Wait for element to be ready, then type
                await self.page.wait_for_selector(selector, timeout=2000)
                await self.page.fill(selector, value)
                return {"status": "typed", "value": value}
            
            elif action_type == "click":
                # Wait for element, then click
                await self.page.wait_for_selector(selector, timeout=2000)
                await self.page.click(selector)
                return {"status": "clicked"}
                
            elif action_type == "reset":
                await self.page.reload()
                return {"status": "reset"}
                
        except Exception as e:
            print(f"Action Failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()