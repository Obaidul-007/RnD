import pytest
from playwright.sync_api import Page, expect

def test_page_loads(page: Page):
    """Test that the main page loads successfully"""
    expect(page).to_have_title("Task Manager")
    expect(page.locator("h1")).to_contain_text("Task Manager")

def test_initial_tasks_display(page: Page):
    """Test that initial tasks are displayed"""
    tasks = page.locator(".task")
    expect(tasks).to_have_count(3)

def test_add_new_task(page: Page):
    """Test adding a new task"""
    # Fill in new task
    page.fill("#new-task", "Test Task from Playwright")
    
    # Click add button
    page.click("button:has-text('Add Task')")
    
    # Wait for page reload and verify task was added
    page.wait_for_load_state("networkidle")
    expect(page.locator(".task")).to_have_count(4)
    expect(page.locator(".task")).to_contain_text("Test Task from Playwright")

def test_complete_task(page: Page):
    """Test completing a task"""
    # Click complete button for first incomplete task
    incomplete_task = page.locator(".task:not(.completed)").first
    complete_button = incomplete_task.locator("button:has-text('Complete')")
    complete_button.click()
    
    # Wait for page reload and verify task is completed
    page.wait_for_load_state("networkidle")
    expect(page.locator(".task.completed")).to_have_count_greater_than(1)

def test_delete_task(page: Page):
    """Test deleting a task"""
    initial_count = page.locator(".task").count()
    
    # Click delete button for first task
    delete_button = page.locator(".task button:has-text('Delete')").first
    delete_button.click()
    
    # Wait for page reload and verify task was deleted
    page.wait_for_load_state("networkidle")
    expect(page.locator(".task")).to_have_count(initial_count - 1)