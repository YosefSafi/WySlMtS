import os
from typing import List, Optional
from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self, openai_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file.")
        
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        if self.tavily_api_key:
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
        else:
            self.tavily_client = None

    def _web_search(self, query: str) -> str:
        """
        Perform a web search using Tavily.
        """
        if not self.tavily_client:
            return "Web search is disabled (TAVILY_API_KEY not set)."
        
        search_result = self.tavily_client.search(query=query, search_depth="advanced", max_results=5)
        
        context = []
        for result in search_result.get("results", []):
            context.append(f"Source: {result['url']}\nContent: {result['content']}")
        
        return "\n\n".join(context)

    def research_topic(self, topic: str) -> str:
        """
        Perform a research-style summary of a topic using Web Search and OpenAI.
        """
        search_context = ""
        if self.tavily_client:
            search_context = self._web_search(topic)
        
        prompt = f"""
        You are a highly efficient research assistant. 
        I want you to research the following topic: "{topic}"
        
        I have gathered the following real-time information from the web to help you:
        ---
        {search_context}
        ---
        
        Based on the above context (if provided) and your internal knowledge, provide a concise, professional, and actionable summary.
        
        The summary should include:
        1. Key points/concepts (citing sources if possible).
        2. Potential action items or next steps.
        3. A brief conclusion.
        
        Format the output clearly for a CLI interface using Markdown.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional research assistant with web search capabilities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content or "No summary generated."

    def summarize_day(self, tasks_summary: str) -> str:
        """
        Generate a daily productivity summary based on completed and pending tasks.
        """
        prompt = f"""
        Based on the following list of tasks and their statuses, generate a daily productivity summary:
        {tasks_summary}
        
        Highlight achievements and suggest focus areas for tomorrow.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a productivity coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content or "No summary generated."
