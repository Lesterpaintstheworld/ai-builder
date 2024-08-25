import logging
import requests
import PyPDF2
import io
from openai import OpenAI

class ResearchCoordinator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = OpenAI()

    def process_paper(self):
        url = self.read_url_from_file()
        self.logger.info(f"Processing paper from URL: {url}")
        try:
            pdf_content = self.download_pdf(url)
            text_content = self.read_pdf(pdf_content)
            analysis = self.analyze_paper(text_content, url)
            post_content = self.create_post(url, analysis)
            self.create_post_file(url, post_content)
            self.logger.info("Paper processing completed")
            return post_content
        except Exception as e:
            self.logger.error(f"Error processing paper: {str(e)}")
            return None

    def read_url_from_file(self):
        try:
            with open('to_analyze.md', 'r') as file:
                url = file.read().strip()
            return url
        except Exception as e:
            self.logger.error(f"Error reading URL from file: {str(e)}")
            raise

    def download_pdf(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)

    def read_pdf(self, pdf_content):
        reader = PyPDF2.PdfReader(pdf_content)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def analyze_paper(self, text, url):
        prompt = f"""
        Perform a detailed Literature Content Analysis (LCA) of the following research paper from {url}. 
        Focus on:
        1. Key findings and their significance
        2. Methodologies used and their appropriateness
        3. Theoretical framework and its application
        4. Data collection and analysis techniques
        5. Limitations of the study
        6. Implications for AI development, especially in the context of autonomous systems
        7. Novel approaches or breakthroughs introduced
        
        Provide a comprehensive and critical analysis, highlighting strengths and potential areas for further research.
        """

        self.logger.info("Analyzer Input:")
        self.logger.info(f"Prompt: {prompt}")
        self.logger.info(f"Text (truncated): {text[:500]}...")

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI research analyst specializing in conducting thorough Literature Content Analysis of complex AI papers."},
                {"role": "user", "content": f"{prompt}\n\nPaper content:\n{text}"}  # Include full text
            ]
        )

        analysis = response.choices[0].message.content
        self.logger.info("Analyzer Output:")
        self.logger.info(f"Analysis: {analysis}")

        return analysis

    def create_post(self, url, analysis):
        prompt = f"""
        Based on the following detailed analysis of a research paper, create an engaging and informative post for the r/autonomousAIs community. The post should:

        1. Start with a catchy title that summarizes the key finding or implication of the paper
        2. Provide a brief introduction that sets the context for the research
        3. Summarize the main points of the analysis in a way that's accessible to a general audience interested in AI
        4. Highlight the implications for autonomous AI systems
        5. Include thought-provoking questions or points for discussion
        6. End with a call-to-action for community engagement

        Make the post engaging, informative, and tailored to the interests of the r/autonomousAIs community. Use markdown formatting for better readability.

        Analysis:
        {analysis}

        Paper URL: {url}
        """

        self.logger.info("Post Writer Input:")
        self.logger.info(f"Prompt: {prompt}")
        self.logger.info(f"Analysis: {analysis}")
        self.logger.info(f"URL: {url}")

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI research communicator specializing in creating engaging posts about AI research for online communities."},
                {"role": "user", "content": prompt}
            ]
        )

        post_content = response.choices[0].message.content
        self.logger.info("Post Writer Output:")
        self.logger.info(f"Post Content: {post_content}")

        return post_content

    def create_post_file(self, url, post_content):
        # Implement file creation logic here
        pass
