from agents.prompt import begin_sentence, agent_prompt
import os
from openai import AsyncOpenAI
from custom_types import (
    ResponseRequiredRequest,
    ResponseResponse,
    Utterance,
)
from typing import List
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# class LLMClient:
#     def __init__(self, retriever, embedding_model="sentence-transformers/paraphrase-MiniLM-L6-v2"):
#         """
#         Initialize the LLMClient with a retriever and embedding model.
#         Args:
#             retriever: Preloaded FAISS retriever instance.
#             embedding_model: HuggingFace embedding model name for compatibility.
#         """
#         self.retriever = retriever
#         self.embedding_model = embedding_model
#         # print(f"OpenAI API Key: {openai_api_key}")        
#         self.client = AsyncOpenAI(
#             api_key=openai_api_key,
#         )

#     def draft_begin_message(self):
#         response = ResponseResponse(
#             response_id=0,
#             content=begin_sentence,
#             content_complete=True,
#             end_call=False,
#         )
#         return response

#     def convert_transcript_to_openai_messages(self, transcript: List[Utterance]):
#         messages = []
#         for utterance in transcript:
#             if utterance.role == "agent":
#                 messages.append({"role": "assistant", "content": utterance.content})
#             else:
#                 messages.append({"role": "user", "content": utterance.content})
#         return messages
    
#     def generate_agent_prompt(self, request: ResponseRequiredRequest):
#         # TODO: Add context from RAG model
#         query = request.transcript[-1].content if request.transcript else ""
#         context = self.retriever.similarity_search(query, k=5)
#         context_text = "\n\n".join([doc.page_content for doc in context])

#         prompt = [
#             {
#                 "role": "system",
#                 "content": f"Hey there, I'm your financial helper. I'm here to make sure you're financially secure. How can I assist you today?\n\n{context_text}",
#             }
#         ]

#         transcript_messages = self.convert_transcript_to_openai_messages(
#             request.transcript
#         )

#         for message in transcript_messages:
#             prompt.append(message)

#         if request.interaction_type == "reminder_required":
#             prompt.append(
#                 {
#                     "role": "user",
#                     "content": "(Now the user has not responded in a while, you would say:)",
#                 }
#             )
#         return prompt

#     async def draft_response(self, request: ResponseRequiredRequest):
#         prompt = self.generate_agent_prompt(request)
#         stream = await self.client.chat.completions.create(
#             model="gpt-4-turbo-preview",  # Or use a 3.5 model for speed
#             messages=prompt,
#             stream=True,
#         )
#         print(f"Prompt being sent to OpenAI for request ID {request.response_id}: {prompt}")

#         accumulated_content = ""

#         async for chunk in stream:
#         # Ensure "choices" and "delta" keys are present in the chunk
#             if chunk.choices and chunk.choices[0].delta.content:
#                 new_content = chunk.choices[0].delta.content
#                 accumulated_content += new_content
#                 # Build and yield the response
#                 response = ResponseResponse(
#                     response_id=request.response_id,
#                     content=new_content,
#                     content_complete=False,
#                     end_call=False,
#                 )
#                 print(f"Response chunk sent: {response}")
#                 yield response


#         # Send final response with "content_complete" set to True to signal completion
#         response = ResponseResponse(
#             response_id=request.response_id,
#             content="",
#             content_complete=True,
#             end_call=False,
#         )
#         yield response
class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )

    def draft_begin_message(self):
        return ResponseResponse(
            response_id=0,
            content=begin_sentence,
            content_complete=True,
            end_call=False,
        )

    def convert_transcript_to_openai_messages(self, transcript: List[Utterance]):
        messages = []
        for utterance in transcript:
            role = "assistant" if utterance.role == "agent" else "user"
            messages.append({"role": role, "content": utterance.content})
        return messages

    def prepare_prompt(self, request: ResponseRequiredRequest):
        prompt = [{"role": "system", "content": agent_prompt}]
        prompt.extend(self.convert_transcript_to_openai_messages(request.transcript))

        if request.interaction_type == "reminder_required":
            prompt.append({
                "role": "user",
                "content": "(Now the user has not responded in a while, you would say:)"
            })
        
        return prompt

    async def draft_response(self, request: ResponseRequiredRequest):
        prompt = self.prepare_prompt(request)
        stream = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Or use a 3.5 model for speed
            messages=prompt,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield ResponseResponse(
                    response_id=request.response_id,
                    content=chunk.choices[0].delta.content,
                    content_complete=False,
                    end_call=False,
                )

        yield ResponseResponse(
            response_id=request.response_id,
            content="",
            content_complete=True,
            end_call=False,
        )
