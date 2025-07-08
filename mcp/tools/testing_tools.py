import asyncio
import json
import subprocess
from typing import Dict, List, Any
from playwright.async_api import async_playwright

class TestingTools:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def generate_test_case(self, url: str, test_type: str, description: str = "") -> Dict[str, Any]:
        """Generate Playwright test cases based on page analysis"""
        analysis = await self.analyze_page(url)
        
        if test_type == "ui":
            test_code = self._generate_ui_test(analysis, description)
        elif test_type == "api":
            test_code = self._generate_api_test(analysis, description)
        elif test_type == "e2e":
            test_code = self._generate_e2e_test(analysis, description)
        else:
            raise ValueError(f"Unknown test type: {test_type}")
        
        return {
            "test_type": test_type,
            "test_code": test_code,
            "analysis": analysis,
            "description": description
        }
    
    async def analyze_page(self, url: str) -> Dict[str, Any]:
        """Analyze web page structure and identify testing opportunities"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.goto(url)
                
                # Extract page information
                title = await page.title()
                forms = await page.query_selector_all("form")
                buttons = await page.query_selector_all("button")
                inputs = await page.query_selector_all("input")
                links = await page.query_selector_all("a")
                
                # Analyze interactive elements
                form_data = []
                for form in forms:
                    form_info = {
                        "action": await form.get_attribute("action") or "",
                        "method": await form.get_attribute("method") or "GET",
                        "inputs": []
                    }
                    form_inputs = await form.query_selector_all("input")
                    for inp in form_inputs:
                        form_info["inputs"].append({
                            "type": await inp.get_attribute("type") or "text",
                            "name": await inp.get_attribute("name") or "",
                            "id": await inp.get_attribute("id") or ""
                        })
                    form_data.append(form_info)
                
                button_data = []
                for button in buttons:
                    button_data.append({
                        "text": await button.text_content() or "",
                        "type": await button.get_attribute("type") or "button",
                        "id": await button.get_attribute("id") or "",
                        "onclick": await button.get_attribute("onclick") or ""
                    })
                
                return {
                    "url": url,
                    "title": title,
                    "forms": form_data,
                    "buttons": button_data,
                    "input_count": len(inputs),
                    "link_count": len(links),
                    "test_opportunities": self._identify_test_opportunities(form_data, button_data)
                }
            
            finally:
                await browser.close()
    
    def _identify_test_opportunities(self, forms: List[Dict], buttons: List[Dict]) -> List[str]:
        """Identify potential test scenarios"""
        opportunities = []
        
        if forms:
            opportunities.append("Form submission testing")
            opportunities.append("Input validation testing")
        
        if buttons:
            opportunities.append("Button click interactions")
            opportunities.append("UI state changes")
        
        opportunities.extend([
            "Page loading performance",
            "Responsive design testing",
            "Accessibility testing",
            "Error handling scenarios"
        ])
        
        return opportunities
    
    def _generate_ui_test(self, analysis: Dict, description: str) -> str:
        """Generate UI test code"""
        return f'''
import pytest
from playwright.sync_api import Page, expect

def test_{description.lower().replace(' ', '_') or 'ui_functionality'}(page: Page):
    """Test UI functionality for {analysis['title']}"""
    page.goto("{analysis['url']}")
    
    # Check page title
    expect(page).to_have_title("{analysis['title']}")
    
    # Test interactive elements
    {self._generate_button_tests(analysis.get('buttons', []))}
    
    # Test forms if present
    {self._generate_form_tests(analysis.get('forms', []))}
'''
    
    def _generate_api_test(self, analysis: Dict, description: str) -> str:
        """Generate API test code"""
        return f'''
import pytest
import requests

def test_{description.lower().replace(' ', '_') or 'api_endpoints'}():
    """Test API endpoints for {analysis['title']}"""
    base_url = "{analysis['url']}"
    
    # Test GET endpoint
    response = requests.get(f"{{base_url}}/api/tasks")
    assert response.status_code == 200
    
    # Test POST endpoint
    new_task = {{"title": "Test Task"}}
    response = requests.post(f"{{base_url}}/api/tasks", json=new_task)
    assert response.status_code == 201
    
    # Test PUT endpoint
    task_id = response.json()["id"]
    updated_task = {{"title": "Updated Task", "completed": True}}
    response = requests.put(f"{{base_url}}/api/tasks/{{task_id}}", json=updated_task)
    assert response.status_code == 200
    
    # Test DELETE endpoint
    response = requests.delete(f"{{base_url}}/api/tasks/{{task_id}}")
    assert response.status_code == 200
'''
    
    def _generate_e2e_test(self, analysis: Dict, description: str) -> str:
        """Generate end-to-end test code"""
        return f'''
import pytest
from playwright.sync_api import Page, expect

def test_{description.lower().replace(' ', '_') or 'e2e_workflow'}(page: Page):
    """End-to-end test for {analysis['title']}"""
    page.goto("{analysis['url']}")
    
    # Complete user workflow
    {self._generate_workflow_steps(analysis)}
    
    # Verify final state
    expect(page.locator("body")).to_be_visible()
'''
    
    def _generate_button_tests(self, buttons: List[Dict]) -> str:
        """Generate button test code"""
        if not buttons:
            return "# No buttons found"
        
        tests = []
        for button in buttons[:3]:  # Test first 3 buttons
            if button['text']:
                tests.append(f"    page.click('text={button['text']}')")
        
        return '\n'.join(tests) if tests else "# No clickable buttons found"
    
    def _generate_form_tests(self, forms: List[Dict]) -> str:
        """Generate form test code"""
        if not forms:
            return "# No forms found"
        
        tests = []
        for form in forms[:2]:  # Test first 2 forms
            for inp in form['inputs']:
                if inp['type'] == 'text' and inp['name']:
                    tests.append(f"""    page.fill("input[name=\\"{inp['name']}\\"]", "test value")""")
        
        return '\n'.join(tests) if tests else "# No form inputs found"
    
    def _generate_workflow_steps(self, analysis: Dict) -> str:
        """Generate workflow test steps"""
        steps = [
            '    # Step 1: Verify page loads',
            f"    expect(page).to_have_title(\"{analysis['title']}\")",
            '',
            '    # Step 2: Interact with elements',
        ]
        
        if analysis.get('forms'):
            steps.append('    # Fill form if present')
            steps.append('    page.fill("input[type=\\"text\\"]", "test input")')
        
        if analysis.get('buttons'):
            steps.append('    # Click buttons')
            steps.append('    page.click("button")')
        
        return '\n'.join(steps)
    
    async def run_test_suite(self, test_file: str, browser: str = "chromium") -> Dict[str, Any]:
        """Run Playwright test suite"""
        try:
            cmd = f"pytest {test_file} --browser {browser} --html=reports/report.html --self-contained-html"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "test_file": test_file,
                "browser": browser
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "test_file": test_file,
                "browser": browser
            }