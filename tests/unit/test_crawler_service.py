import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
from services.crawler import Crawler

@pytest.mark.asyncio
async def test_crawl_website():
    # Arrange
    repository_mock = MagicMock()
    logger_mock = MagicMock()
    crawler = Crawler(
            repository=repository_mock, 
            base_dir=Path("/tmp"), 
            logger=logger_mock)
    
    start_url = "https://example.com"
    number_of_links = 5
    run_id = "test_run_id"
    
    with patch("utils.context_managers.BrowserContextManager") as mock_browser_manager, \
         patch("utils.context_managers.PageContextManager") as mock_page_manager:
        
        mock_browser = mock_browser_manager.return_value.__aenter__.return_value
        mock_page = mock_page_manager.return_value.__aenter__.return_value
        mock_page.evaluate.return_value = ["https://example.com/link1", 
                                           "https://example.com/link2",
                                           "https://example.com/link3",
                                           "https://example.com/link4",]
        
        mock_screenshot_paths = [
                    f"/tmp/{run_id}_screenshot_0.png",
                    f"/tmp/{run_id}_screenshot_1.png"
                    ]
        crawler.take_screenshots = AsyncMock(return_value=mock_screenshot_paths)

        # Act
        screenshots = await crawler.crawl_website(start_url, number_of_links, run_id)

        # Assert
        crawler.take_screenshots.assert_called_once_with(
            [start_url] + mock_page.evaluate.return_value,
            mock_browser,
            run_id,
            {
                "run_id": run_id,
                "start_url": start_url,
                "number_of_links": number_of_links,
                "links": [start_url] + mock_page.evaluate.return_value
            }
        )
        repository_mock.insert_screenshot_data.assert_called_once_with(
            run_id, start_url, mock_screenshot_paths
        )
        assert screenshots == mock_screenshot_paths


@pytest.mark.asyncio
async def test_take_screenshots():
    # Arrange
    repository_mock = MagicMock()
    logger_mock = MagicMock()
    crawler = Crawler(repository=repository_mock, base_dir=Path("/tmp"), logger=logger_mock)

    links_to_pages = ["https://example.com/link1", "https://example.com/link2"]
    browser_mock = MagicMock()
    run_id = "test_run_id"

    crawler._take_screenshot = AsyncMock(side_effect=[
        "/tmp/test_run_id_screenshot_0.png",
        "/tmp/test_run_id_screenshot_1.png"
    ])

    # Act
    screenshot_paths = await crawler.take_screenshots(links_to_pages, browser_mock, run_id, {})

    # Assert
    assert screenshot_paths == [
        "/tmp/test_run_id_screenshot_0.png",
        "/tmp/test_run_id_screenshot_1.png"
    ]
    assert crawler._take_screenshot.call_count == 2


def test_get_screenshots_by_run_id():
    # Arrange
    repository_mock = MagicMock()
    logger_mock = MagicMock()
    crawler = Crawler(repository=repository_mock, base_dir=Path("/tmp"), logger=logger_mock)

    run_id = "test_run_id"
    expected_result = ["screenshot_1.png", "screenshot_2.png"]
    repository_mock.get_screenshots_by_run_id.return_value = expected_result

    # Act
    result = crawler.get_screenshots_by_run_id(run_id)

    # Assert
    assert result == expected_result
    repository_mock.get_screenshots_by_run_id.assert_called_once_with(run_id)


@pytest.mark.asyncio
async def test_take_screenshot():
    # Arrange
    repository_mock = MagicMock()
    logger_mock = MagicMock()
    crawler = Crawler(repository=repository_mock, base_dir=Path("/tmp"), logger=logger_mock)

    url = "https://example.com"
    screenshot_path = Path("/tmp/test_screenshot.png")

    with patch("utils.context_managers.PageContextManager") as mock_page_manager:
        mock_page = mock_page_manager.return_value.__aenter__.return_value
        
        # Act
        result = await crawler._take_screenshot(MagicMock(), url, screenshot_path)

        # Assert
        mock_page.goto.assert_called_once_with(url)
        mock_page.screenshot.assert_called_once_with(path=str(screenshot_path))
        assert result == str(screenshot_path)