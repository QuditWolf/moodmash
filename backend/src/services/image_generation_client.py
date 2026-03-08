"""
Image Generation Client for AWS Bedrock

Supports multiple image generation models:
- Amazon Titan Image Generator
- Stability AI Stable Diffusion XL
"""

import json
import base64
import logging
import os
from typing import Dict, Any, Optional
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class ImageGenerationClient:
    """Client for generating images using AWS Bedrock."""
    
    def __init__(self):
        """Initialize Bedrock runtime client for image generation."""
        # Get configuration from environment
        region = os.getenv('AWS_REGION', 'us-east-1')
        endpoint_url = os.getenv('BEDROCK_ENDPOINT')
        
        logger.info(f"Initializing Image Generation Client for region: {region}")
        
        # Configure retry logic
        config = Config(
            region_name=region,
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            }
        )
        
        # Initialize client
        if endpoint_url:
            self.client = boto3.client(
                'bedrock-runtime',
                endpoint_url=endpoint_url,
                config=config
            )
            logger.info(f"Initialized Bedrock client with custom endpoint: {endpoint_url}")
        else:
            self.client = boto3.client('bedrock-runtime', config=config)
            logger.info(f"Initialized Bedrock client for region: {region}")
    
    def generate_with_titan(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        cfg_scale: float = 8.0,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate image using Amazon Titan Image Generator.
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the image
            width: Image width (512, 768, 1024)
            height: Image height (512, 768, 1024)
            cfg_scale: How closely to follow the prompt (1.0-10.0)
            seed: Random seed for reproducibility
            
        Returns:
            Dictionary with 'image' (base64) and 'metadata'
            
        Raises:
            Exception: If generation fails
        """
        try:
            model_id = os.getenv('TITAN_IMAGE_MODEL', 'amazon.titan-image-generator-v2:0')
            
            # Build request body
            body = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "width": width,
                    "height": height,
                    "cfgScale": cfg_scale
                }
            }
            
            if negative_prompt:
                body["textToImageParams"]["negativeText"] = negative_prompt
            
            if seed is not None:
                body["imageGenerationConfig"]["seed"] = seed
            
            logger.info(f"Generating image with Titan: {width}x{height}, cfg_scale={cfg_scale}")
            
            # Call Bedrock
            response = self.client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if 'images' not in response_body or len(response_body['images']) == 0:
                raise ValueError("No images returned from Titan")
            
            image_base64 = response_body['images'][0]
            
            logger.info("Image generated successfully with Titan")
            
            return {
                "image": image_base64,
                "format": "png",
                "model": model_id,
                "width": width,
                "height": height
            }
            
        except ClientError as e:
            logger.error(f"AWS Bedrock error: {e}", exc_info=True)
            raise Exception(f"Failed to generate image with Titan: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            raise
    
    def generate_with_nova(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        cfg_scale: float = 8.0,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate image using Amazon Nova Canvas.
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the image
            width: Image width (256-1408, multiple of 64)
            height: Image height (256-1408, multiple of 64)
            cfg_scale: How closely to follow the prompt (1.1-10.0)
            seed: Random seed for reproducibility (0-858993459)
            
        Returns:
            Dictionary with 'image' (base64) and 'metadata'
            
        Raises:
            Exception: If generation fails
        """
        try:
            model_id = os.getenv('NOVA_CANVAS_MODEL', 'amazon.nova-canvas-v1:0')
            
            # Build request body
            body = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "width": width,
                    "height": height,
                    "cfgScale": cfg_scale,
                    "quality": "premium"
                }
            }
            
            if negative_prompt:
                body["textToImageParams"]["negativeText"] = negative_prompt
            
            if seed is not None:
                body["imageGenerationConfig"]["seed"] = seed
            
            logger.info(f"Generating image with Nova Canvas: {width}x{height}, cfg_scale={cfg_scale}")
            
            # Call Bedrock
            response = self.client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if 'images' not in response_body or len(response_body['images']) == 0:
                raise ValueError("No images returned from Nova Canvas")
            
            image_base64 = response_body['images'][0]
            
            logger.info("Image generated successfully with Nova Canvas")
            
            return {
                "image": image_base64,
                "format": "png",
                "model": model_id,
                "width": width,
                "height": height
            }
            
        except ClientError as e:
            logger.error(f"AWS Bedrock error: {e}", exc_info=True)
            raise Exception(f"Failed to generate image with Nova Canvas: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            raise
    
    def generate_with_stable_diffusion(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        cfg_scale: float = 7.0,
        steps: int = 50,
        seed: Optional[int] = None,
        style_preset: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate image using Stability AI Stable Diffusion XL.
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the image
            width: Image width (must be multiple of 64, max 1536)
            height: Image height (must be multiple of 64, max 1536)
            cfg_scale: How closely to follow the prompt (0-35)
            steps: Number of diffusion steps (10-150)
            seed: Random seed for reproducibility (0-4294967295)
            style_preset: Style preset (e.g., 'photographic', 'digital-art', 'comic-book')
            
        Returns:
            Dictionary with 'image' (base64) and 'metadata'
            
        Raises:
            Exception: If generation fails
        """
        try:
            model_id = os.getenv('SDXL_MODEL', 'stability.stable-diffusion-xl-v1')
            
            # Build request body
            body = {
                "text_prompts": [
                    {"text": prompt, "weight": 1.0}
                ],
                "cfg_scale": cfg_scale,
                "steps": steps,
                "width": width,
                "height": height
            }
            
            if negative_prompt:
                body["text_prompts"].append({"text": negative_prompt, "weight": -1.0})
            
            if seed is not None:
                body["seed"] = seed
            
            if style_preset:
                body["style_preset"] = style_preset
            
            logger.info(f"Generating image with SDXL: {width}x{height}, steps={steps}, cfg_scale={cfg_scale}")
            
            # Call Bedrock
            response = self.client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if 'artifacts' not in response_body or len(response_body['artifacts']) == 0:
                raise ValueError("No images returned from Stable Diffusion")
            
            image_base64 = response_body['artifacts'][0]['base64']
            finish_reason = response_body['artifacts'][0].get('finishReason', 'SUCCESS')
            
            if finish_reason != 'SUCCESS':
                logger.warning(f"Image generation finished with reason: {finish_reason}")
            
            logger.info("Image generated successfully with Stable Diffusion XL")
            
            return {
                "image": image_base64,
                "format": "png",
                "model": model_id,
                "width": width,
                "height": height,
                "finish_reason": finish_reason
            }
            
        except ClientError as e:
            logger.error(f"AWS Bedrock error: {e}", exc_info=True)
            raise Exception(f"Failed to generate image with Stable Diffusion: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            raise
    
    def generate_image(
        self,
        prompt: str,
        model: str = "titan",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using specified model.
        
        Args:
            prompt: Text description of the image
            model: Model to use ('titan', 'nova', or 'sdxl')
            **kwargs: Model-specific parameters
            
        Returns:
            Dictionary with image data and metadata
        """
        if model.lower() == "titan":
            return self.generate_with_titan(prompt, **kwargs)
        elif model.lower() == "nova":
            return self.generate_with_nova(prompt, **kwargs)
        elif model.lower() in ["sdxl", "stable-diffusion", "stability"]:
            return self.generate_with_stable_diffusion(prompt, **kwargs)
        else:
            raise ValueError(f"Unknown model: {model}. Use 'titan', 'nova', or 'sdxl'")


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    client = ImageGenerationClient()
    
    # Test prompt
    test_prompt = "A highly detailed digital collage art piece featuring a young person with headphones in a dreamy, surreal environment with torn paper textures and indie zine aesthetic"
    
    try:
        result = client.generate_image(test_prompt, model="titan", width=1024, height=1024)
        print(f"Generated image: {len(result['image'])} bytes (base64)")
        print(f"Model: {result['model']}")
    except Exception as e:
        print(f"Error: {e}")
