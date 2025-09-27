from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.custom_tool import BraveSearchTool
from dotenv import load_dotenv
import os
import re

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def save_report_callback(output):
    """Callback function to save the report with a dynamic filename."""
    markdown_content = output.raw
    
    # Find the first non-empty line to use as the title.
    # If no content, use a default name.
    title_line = next((line.strip() for line in markdown_content.split('\n') if line.strip()), "Untitled_Report")
    
    # Sanitize the title to create a valid filename.
    # Remove markdown heading characters and clean up.
    filename_base = title_line.lstrip('# ').strip()
    # Replace spaces and invalid characters.
    sanitized_filename = re.sub(r'[^\w\s-]', '', filename_base).strip().replace(' ', '_')
    filename = f"{sanitized_filename}.md"

    # Save the report to a file in the root directory.
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"\n\n[crewai] Report saved as: {filename}")

@CrewBase
class CrewaiBravesearch():
	"""CrewaiBravesearch crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[BraveSearchTool()],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			callback=save_report_callback
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiBravesearch crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)


	