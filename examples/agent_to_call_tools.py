import os
import asyncio
from typing import List

from mcp import ClientSession, StdioServerParameters
from langchain.agents import create_agent

from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

# os.environ["GOOGLE_API_KEY"] = "your_key" # Force a specific gemini api key

async def process_query_agent(session: ClientSession, query: str) -> List:
    # LLM Model driver alternatives
    
    model_name = "llama3.2"
    model_name = "qwen3.5:4b"
    model = ChatOllama( model = model_name, temperatur = 0 )

    model_name = "gemini-2.5-flash"
    model_name = "gemini-3.1-flash-lite-preview"
    model = ChatGoogleGenerativeAI( model = model_name, temperature = 0 )

    response = await session.list_tools()
    tools = response.tools
    name_tools_str = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
    print(name_tools_str)
    
    tools = await load_mcp_tools(session)
    system_prompt = f"""
    You are a helpful assistant that can use the following tools to answer questions: {name_tools_str}
    If you need to use a tool, call it using the tool name and the arguments.
    
    The tools help you to extract, map or suggest EDAM ontology concepts given a textual description.
    You can also query the biotools database to search a tool for the user, according to his keywords.
    
    The EDAM ontology describes concepts concerning scientific data analysis ad data management, it is divided into four categories of concepts: topics, operations, data identifiers and formats.
    """

    final_text = []
    agent = create_agent( model, tools, system_prompt=system_prompt,)
    msgs = { "messages": [{"role": "user", "content": query}] }
    response = await agent.ainvoke(msgs)

    res = []
    for i in range(len(response["messages"])):
        r = response["messages"][i].content
        print(r)
        res.append(r)
    #return "\n".join(final_text)
    return res

async def main() -> None:
    path_edammcp_repo = "/path/to/repo/edammcp"
    
    client = MultiServerMCPClient(
        {
            "edam-mcp": {
              "transport": "stdio",
              "command": "uv",
              "args": [
                "--directory",
                "{path_edammcp_repo}",
                "run",
                "edam-mcp"
              ],
              "env": {
                "EDAM_SIMILARITY_THRESHOLD": "0.7"
              }
            }
        }
    )

    async with client.session("edam-mcp") as session:
        # test mapping
        query = "Map the following description to edam ontology concepts: \n\n \"A robust, scalable pipeline to run Boltz-2 (https://github.com/jwohlwend/boltz) structure predictions with advanced complex modeling, ligand support, and structural constraints, with local multiple sequence alignment (MSA) using Nextflow. nf-boltz-2 orchestrates Boltz structure prediction, handling input preparation, resource management, sequences/ligands complexity, and advanced configuration for constraints and templates. This pipeline runs every step in an Apptainer/Singularity container.\""
        
        # test mapping
        query = "Map the following description: 'The variant calling function takes as input a database of regulation genes and expands their netwok using STRING db.'"
        
        # test query biotools
        query = "search 'variant calling' tools in biotools"
        
        # test suggestion
        query = "Introduce the concept cancer surveillance in the correct hierarchy as a topic in EDAM. This concept is a specific application of epidemiology field."
        
        # combining mapping tool call with biotools search
        query = "Map the following description: 'Framework for processing and visualization of chromatographically separated and single-spectra mass spectral data.' and search for similar tools in biotools using the mapped ontology terms"
        
        answer = await process_query_agent(session, query)
        print("\nAnswer:", answer)

if __name__ == "__main__":
    asyncio.run(main())
