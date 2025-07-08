import pytest
import asyncio
from playwright.sync_api import Page, expect
from mcp.tools.testing_tools import TestingTools

class TestAIPowered:
    def setup_method(self):
        self.testing_tools = TestingTools()
    
    @pytest.mark.asyncio
    async def test_ai_page_analysis(self, page: Page):
        """Test AI-powered page analysis"""
        url = page.url
        analysis = await self.testing_tools.analyze_page(url)
        
        assert analysis["title"] == "Task Manager"
        assert len(analysis["forms"]) > 0
        assert len(analysis["buttons"]) > 0
        assert "Form submission testing" in analysis["test_opportunities"]
    
    @pytest.mark.asyncio
    async def test_ai_test_generation(self, page: Page):
        """Test AI-powered test case generation"""
        url = page.url
        test_case = await self.testing_tools.generate_test_case(
            url, "ui", "Task management functionality"
        )
        
        assert test_case["test_type"] == "ui"
        assert "def test_" in test_case["test_code"]
        assert "page.goto" in test_case["test_code"]
    
    def test_responsive_design(self, page: Page):
        """Test responsive design with AI insights"""
        # Test desktop view
        page.set_viewport_size({"width": 1920, "height": 1080})
        expect(page.locator("body")).to_be_visible()
        
        # Test tablet view
        page.set_viewport_size({"width": 768, "height": 1024})
        expect(page.locator("body")).to_be_visible()
        
        # Test mobile view
        page.set_viewport_size({"width": 375, "height": 667})
        expect(page.locator("body")).to_be_visible()
    
    def test_accessibility_features(self, page: Page):
        """Test accessibility features"""
        # Check for proper heading structure
        expect(page.locator("h1")).to_have_count(1)
        
        # Check for form labels (implicit or explicit)
        expect(page.locator("input")).to_have_count_greater_than(0)
        
        # Check for button text
        buttons = page.locator("button")
        for i in range(buttons.count()):
            button = buttons.nth(i)
            expect(button).not_to_have_text("")