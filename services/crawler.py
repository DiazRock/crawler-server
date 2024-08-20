import asyncio

class Crawler:
    def __init__(self, collection, base_dir: str):
        self.collection = collection
        self.base_dir = base_dir

    async def take_screenshots(self, start_url: str, number_of_links: int, run_id: str):
        # Simulate an asynchronous task, e.g., fetching a URL and taking a screenshot
        screenshots = []
        for i in range(number_of_links + 1):
            screenshot_filename = f"{run_id}_screenshot_{i}.png"
            screenshot_path = self.base_dir / screenshot_filename
            
            # Simulate the delay for taking a screenshot
            await asyncio.sleep(1)  # Replace this with actual screenshot logic
            
            # Create a dummy screenshot file
            with open(screenshot_path, "w") as f:
                f.write("This is a dummy screenshot file.")
            
            screenshots.append(screenshot_filename)

        # Save the screenshots to MongoDB
        self.collection.insert_one({"_id": run_id, "screenshots": screenshots})

        return screenshots
