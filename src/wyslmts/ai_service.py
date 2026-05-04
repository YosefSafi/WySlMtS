import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file.")
        self.client = OpenAI(api_key=self.api_key)

    def research_topic(self, topic: str) -> str:
        """
        Perform a research-style summary of a topic using OpenAI.
        """
        prompt = f"""
        You are a highly efficient research assistant. 
        Provide a concise, professional, and actionable summary of the following topic:
        "{topic}"
        
        The summary should include:
        1. Key points/concepts.
        2. Potential action items or next steps.
        3. A brief conclusion.
        
        Format the output clearly for a CLI interface.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional research assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content or "No summary generated."

    def summarize_day(self, tasks_summary: str) -> str:
        """
        Generate a daily summary based on completed and pending tasks.
        """
        prompt = f"""
        Based on the following list of tasks and their statuses, generate a daily productivity summary:
        {tasks_summary}
        
        Highlight achievements and suggest focus areas for tomorrow.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a productivity coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content or "No summary generated."
