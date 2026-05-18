import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:

    def __init__(self):

        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is taken from a company's careers page.

            Your task is to extract all job postings and return them in valid JSON format.

            Each job object must contain:
            - role
            - experience
            - skills
            - description

            Only return valid JSON.
            Do not add explanations or preamble.

            ### VALID JSON:
            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(
            input={"page_data": cleaned_text}
        )

        try:

            json_parser = JsonOutputParser()

            res = json_parser.parse(res.content)

        except OutputParserException:

            raise OutputParserException(
                "Unable to parse jobs. Context may be too large."
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:

            You are Harshini, an AI Solutions Consultant at HireReach AI.

            HireReach AI is an AI-powered software consulting and automation company
            specializing in:
            - AI solutions
            - Workflow automation
            - Scalable software systems
            - Web applications
            - Process optimization
            - Cost reduction

            Write a professional and personalized cold email to the client regarding
            the job opportunity above.

            Highlight how HireReach AI can help fulfill their technical requirements.

            Also include the most relevant portfolio links from:
            {link_list}

            Keep the email concise, professional, and impactful.

            Do not include any preamble.

            ### EMAIL:
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links
        })

        return res.content


if __name__ == "__main__":

    print(os.getenv("GROQ_API_KEY"))