import asyncio
from playwright.async_api import async_playwright
from fake_useragent import UserAgent

# --- CSS TO HIDE ADS & VIDEO PLAYERS ---
async def inject_stealth_css(page):
    try:
        await page.add_style_tag(content="""
            .adsbygoogle, .fc-ab-root, .modal, .popup, .overlay, 
            div[id^="google_ads"], ins, .interstitial,
            video, .jwplayer, .sticky-video, #floating-video {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                pointer-events: none !important;
            }
        """)
    except:
        pass

async def safe_click(page, selector):
    try:
        btn = await page.wait_for_selector(selector, state="visible", timeout=5000)
        # JS Click is best for Linkpays
        await page.evaluate("(el) => el.click()", btn)
        return True
    except:
        return False

async def run_fixed_bot(target_url):
    ua = UserAgent()
    async with async_playwright() as p:
        # Browser launch settings
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent=ua.random,
            viewport={'width': 375, 'height': 812},
            device_scale_factor=2,
            ignore_https_errors=True
        )
        
        page = await context.new_page()
        print(f"🚀 Fixed Bot Started (Target: 6 Cycles): {target_url}")
        
        try:
            await page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
        except:
            print("Page load timeout (continuing)...")

        # --- FIXED LOOP (1 to 6) ---
        for cycle in range(1, 7):
            print(f"\n🔄 Running Cycle #{cycle}...")
            
            # 1. New Tab Setup (Hamesha latest tab par focus)
            current_page = context.pages[-1]
            await current_page.bring_to_front()
            await inject_stealth_css(current_page)
            
            # 2. Timer Wait (25 Seconds Fixed)
            print("⏳ Waiting 25 seconds for timer...")
            await asyncio.sleep(25)
            
            # 3. Scroll Down
            print("👇 Scrolling to find button...")
            await current_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)
            # Screenshot line removed here
            
            # 4. Button Click Logic
            selectors = [
                "text='Continue to Content'", # Cycle 1 Special
                "button:has-text('Get Link')", # Final Link
                "a:has-text('Get Link')",
                "button:has-text('Continue')", 
                ".btn-primary", 
                "a:has-text('Continue')",
                "div:has-text('Continue') >> nth=-1"
            ]
            
            clicked = False
            for sel in selectors:
                if await safe_click(current_page, sel):
                    print(f"✅ Clicked button matching: {sel}")
                    clicked = True
                    
                    # --- CYCLE 6 SPECIAL HANDLING ---
                    if cycle == 6:
                        print("\n🏁 Cycle 6 Clicked! Waiting for Destination URL...")
                        # Thoda wait taaki naya URL load ho jaye
                        await asyncio.sleep(10)
                        
                        # Final Tab Check
                        final_page = context.pages[-1]
                        await final_page.bring_to_front()
                        
                        final_url = final_page.url
                        print(f"\n🎉 FINAL DESTINATION URL: {final_url}")
                        print(f"📄 Page Title: {await final_page.title()}")
                        
                        # Screenshot removed here
                        print("✅ Script Finished Successfully.")
                        await browser.close()
                        return # Script yahi khatam
                    
                    # Agar Cycle 6 nahi hai, to wait karo next page ka
                    await asyncio.sleep(8) 
                    break 
            
            if not clicked:
                print(f"❌ Cycle {cycle}: No button found. Reloading page...")
                await current_page.reload()
                await asyncio.sleep(10)
        
        await browser.close()

if __name__ == "__main__":
    link = "https://linkpays.in/uENkzZ"
    asyncio.run(run_fixed_bot(link))
                      
