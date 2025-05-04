import torch
from diffusers import AutoPipelineForText2Image
from diffusers.utils import load_image
from transformers import T5EncoderModel, TorchAoConfig
from diffusers import FluxTransformer2DModel

name_or_path = "ostris/Flex.2-preview"

inpaint_image = load_image("https://ostris.com/wp-content/uploads/2025/04/dog.jpg")
inpaint_mask = load_image("https://ostris.com/wp-content/uploads/2025/04/dog_mask.jpg")
control_image = load_image("https://ostris.com/wp-content/uploads/2025/04/dog_depth.jpg")

dtype = torch.bfloat16

quant_config = TorchAoConfig("int8_weight_only")

text_encoder_2 = T5EncoderModel.from_pretrained(
    name_or_path, subfolder="text_encoder_2", torch_dtype=dtype, quantization_config=quant_config
).to("cuda")

transformer = FluxTransformer2DModel.from_pretrained(
    name_or_path, subfolder="transformer", torch_dtype=dtype, quantization_config=quant_config
).to("cuda")


pipe = AutoPipelineForText2Image.from_pretrained(
    name_or_path,
    transformer=transformer,
    text_encoder_2=text_encoder_2,
    custom_pipeline=name_or_path,
    torch_dtype=dtype
).to("cuda")

image = pipe(
    prompt="A white friendly robotic dog sitting on a bench",
    inpaint_image=inpaint_image,
    inpaint_mask=inpaint_mask,
    control_image=control_image,
    control_strength=0.5,
    control_stop=0.33,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    num_inference_steps=50,
    generator=torch.Generator("cpu").manual_seed(42)
).images[0]
image.save(f"robot_dog.png")
