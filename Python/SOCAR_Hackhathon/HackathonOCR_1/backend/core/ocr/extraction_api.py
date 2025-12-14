# F:\Projects\HackathonOCR\backend\core\ocr\extraction_api.py - FINAL DEBUG VERSION

import base64
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from openai import OpenAI, APIError
from backend.config.settings import settings
import json # Used for safe JSON decoding

class BaseOCRExtractor(ABC):
    """
    Abstract interface for any OCR/VLM model extractor. 
    """
    @abstractmethod
    def extract_markdown(self, image_bytes: bytes) -> str:
        """
        Takes processed image bytes and calls the VLM API to return the Markdown text.
        """
        pass


class DeepSeekR1Extractor(BaseOCRExtractor):
    """
    Concrete implementation to extract structured Markdown text using the 
    OpenAI SDK structure, confirmed to work with the unified Azure endpoint.
    """
    def __init__(self):
        # 1. Initialize the OpenAI client using unified Azure credentials
        self.base_url = settings.BASE_URL
        
        # Azure SDK compatibility requires the '/openai/v1/' suffix
        if not self.base_url.endswith("/openai/v1/"):
             self.base_url = self.base_url.rstrip("/") + "/openai/v1/"
             
        # Initialize the client using the unified credentials
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=settings.API_KEY,
        )
        
        self.model_name = settings.OCR_MODEL_NAME # Deployment ID from .env
        
        self.system_prompt = (
            "You are an expert OCR and document structure analyst. Your task is to accurately "
            "transcribe the provided document image, which may contain low-quality, noisy, "
            "or multilingual text (Cyrillic/Russian/Azerbaijani). "
            "You MUST convert the entire content, including headings, lists, and tables, "
            "into valid Markdown format, preserving the logical reading order and document structure."
        )

    def extract_markdown(self, image_bytes: bytes) -> str:
        """
        Encodes the image to Base64 and calls the VLM API via the OpenAI SDK.
        """
        if not settings.API_KEY or not settings.BASE_URL:
            return "OCR_ERROR: Unified Azure API Key or BASE_URL is missing or invalid in .env"

        # --- DEBUG CHECK 1: Confirm image data integrity and size ---
        if not image_bytes:
            print("DEBUG: Image bytes is empty!")
            return "OCR_ERROR: Input image bytes were empty."
        print(f"DEBUG: Image bytes size: {len(image_bytes) / 1024:.2f} KB (Before Base64 Encoding)")
        # -----------------------------------------------------------

        # 1. Encode image to Base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Use the confirmed MIME type for your preprocessed images
        mime_type = "image/jpeg"
        image_data_uri = f"data:{mime_type};base64,{base64_image}"
        
        # --- DEBUG CHECK 2: Inspect the URI prefix ---
        print(f"DEBUG: Data URI prefix (first 50 chars): {image_data_uri[:50]}...")
        # ---------------------------------------------
        
        # 2. Construct the multimodal payload
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [
                {
                    "type": "text", 
                    "text": "Please perform high-accuracy OCR and convert this image to Markdown."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # Using the correct data URI format
                        "url": image_data_uri 
                    }
                }
            ]}
        ]
        
        try:
            # 3. Use the working SDK method 
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                # temperature=0.0,
                timeout=60
            )
            
            # 4. Extract the content
            markdown_content = completion.choices[0].message.content
            
            # --- DEBUG CHECK 3: Check for the placeholder response ---
            if "Since I cannot process actual image files" in markdown_content or "upload the image file" in markdown_content:
                print("\nALERT: Received generic placeholder response. VLM did not process the image.")
                print(f"Probable Cause: Base64 payload size limit or deployment configuration failure.")
            # ---------------------------------------------------------
            
            return markdown_content
            
        except APIError as e:
            # Handle API errors (404, 401, 500, 429) raised by the SDK
            status_code = getattr(e, 'status_code', 'Unknown')
            
            # --- CRITICAL FIX: Safe JSON decoding to prevent JSONDecodeError ---
            error_details = 'No error details provided by the API.'
            try:
                # Attempt to safely parse the error JSON
                error_response = e.response.json()
                error_details = error_response.get('error', {}).get('message', 'No detailed message.')
            except json.JSONDecodeError:
                # If JSON decoding fails, try to get raw text content
                error_details = e.response.text or 'Invalid JSON response received.'
            except Exception:
                 pass # Fallback to default message
            # -----------------------------------------------------------------

            print(f"\nFATAL API ERROR: HTTP {status_code}. Details: {error_details[:200]}...") 
            
            # Report the error code and specific details
            if status_code == 404:
                return f"OCR_ERROR: HTTP 404 - Model '{self.model_name}' not found. Check Azure Deployment ID. Details: {error_details}"
            if status_code == 401:
                return f"OCR_ERROR: HTTP 401 - Unauthorized. Check API Key in .env. Details: {error_details}"
            if status_code == 429:
                return f"OCR_ERROR: HTTP 429 - Rate Limit Exceeded. Details: {error_details}"
            if status_code == 500:
                return f"OCR_ERROR: HTTP 500 - Internal Server Error. Issue with VLM processing payload size or complexity. Details: {error_details}"
            
            return f"OCR_ERROR: Azure API Failure. Status: {status_code}. Details: {error_details}"
            
        except Exception as e:
            # Handle general errors (connection, SDK misconfiguration)
            return f"OCR_ERROR: General failure during API call: {e}"