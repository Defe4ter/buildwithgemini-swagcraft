"""Tools for the SwagCraft agent."""

import os
import random
import uuid
from google import genai
from google.cloud import storage

BUCKET_NAME = os.environ.get("SWAG_BUCKET_NAME", "bwg3-qwiklabs-gcp-04-cf18a37c5cc8")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-cf18a37c5cc8")

SURPRISE_SWAG_ITEMS = [
    "Matte Powder-Coated Insulated Steel Water Bottle",
    "Premium Embroidered Heavyweight French Terry Hoodie",
    "Rugged Canvas Chore Work Jacket with Corduroy Collar",
    "Custom Mechanical Keyboard with Anodized Aluminum Chassis",
    "Studio Wireless Over-Ear Noise-Canceling Headphones",
    "Vintage Unstructured Embroidered Corduroy Cap",
    "Handcrafted Speckled Ceramic Stoneware Coffee Mug",
    "Heavyweight 16oz Reinforced Cotton Canvas Everyday Tote",
    "Slim Anodized Magnetic Wireless Power Bank",
    "Linen Hardcover Foil-Stamped Dot-Grid Journal Set",
    "Merino Wool & Vegan Leather Minimalist Desk Pad",
    "Recycled Ripstop Technical Studio Windbreaker",
]


def pick_surprise_item() -> str:
    """Randomly selects a swag item when the user requests 'surprise me' or hasn't picked a specific item.

    Returns:
        A creative swag item name from the swag catalog.
    """
    item = random.choice(SURPRISE_SWAG_ITEMS)
    return item


def generate_swag_mockup(
    company_name: str,
    item_name: str,
    design_concept: str,
    milestone_context: str = "",
    backdrop_color: str = "",
) -> str:
    """Generates a realistic commercial product mockup photo using Nano Banana 2 (gemini-3.1-flash-lite-image)
    and uploads it to public Cloud Storage for UI display.

    Args:
        company_name: The name of the company.
        item_name: The swag item (e.g., 'steel water bottle', 'heavyweight hoodie', 'chore work jacket', 'custom mechanical keyboard').
        design_concept: Visual details, brand colors, aesthetic, and celebratory milestone logo/graphics.
        milestone_context: Short summary of the company's latest advancement, breakthrough, or news to subtly reflect on the product.
        backdrop_color: A single solid primary color for the seamless studio cyclorama backdrop (e.g., 'vibrant electric blue', 'clean studio pastel mint', 'rich brand coral', 'deep cobalt', 'warm studio clay').

    Returns:
        The public HTTPS URL of the generated product mockup image.
    """
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )

    # Determine optimal perspective based on product type
    item_lower = item_name.lower()
    if any(k in item_lower for k in ["bottle", "tumbler", "mug"]):
        perspective = "hero eye-level front-three-quarter view showing the cylindrical form and brand emblem with soft rim reflection"
    elif any(k in item_lower for k in ["hoodie", "windbreaker", "jacket", "coat"]):
        perspective = "clean ghost mannequin studio shot with natural fabric draping, highlighting chest embroidery, custom hardware, and premium tactile texture"
    elif any(k in item_lower for k in ["keyboard"]):
        perspective = "slight elevated 40-degree studio hero shot showing the custom mechanical keycap profile, anodized aluminum chassis, and subtle diffused underglow"
    elif any(k in item_lower for k in ["headphone", "audio"]):
        perspective = "sculptural studio hero shot standing upright on a sleek minimal display pedestal, highlighting the anodized earcups, cushioned headband, and laser-etched emblem"
    elif any(k in item_lower for k in ["cap", "hat"]):
        perspective = "slight elevated 45-degree angle displaying the front crown embroidery and brim curvature"
    elif any(k in item_lower for k in ["desk pad", "mat", "power bank", "charger", "notebook", "journal"]):
        perspective = "elevated 45-degree studio angle with soft natural contact shadow beneath showing refined edge stitching, materials, and ports"
    elif any(k in item_lower for k in ["tote", "bag", "backpack"]):
        perspective = "standing front-angle product shot showing heavy canvas weave, reinforced straps, and structural proportion"
    else:
        perspective = "centered studio beauty shot showcasing clean product contours and proportion"

    milestone_clause = ""
    if milestone_context:
        milestone_clause = (
            f"Commemorative edition: Celebrating {milestone_context}. "
            f"Subtly and tastefully incorporate delicate nods to this milestone into the physical product "
            f"(such as a refined edition accent, subtle laser-etched version badge, commemorative stitch trim, or discrete milestone motif—only if it naturally fits). "
        )

    # Single primary color studio cyclorama backdrop
    bg_color_desc = backdrop_color.strip() if backdrop_color else "a single solid vibrant primary color"
    backdrop_clause = f"Solid seamless {bg_color_desc} cyclorama studio backdrop with an infinite curved wall and floor curve."

    prompt = (
        f"Commercial studio product photography of a single bespoke {item_name} for '{company_name}'. "
        f"Product design and materials: {design_concept}. "
        f"Color palette: Colorful, vibrant, and authentic to '{company_name}' brand identity—the product and materials must NOT be all black, featuring rich brand colors and tactile material textures. "
        f"{milestone_clause}"
        f"Setting: {backdrop_clause} High color contrast between the product and the seamless single-color background so the product really pops out vividly with clean edge separation. "
        f"Lighting: Crisp commercial studio lighting setup with soft overhead key light, subtle edge rim light creating sharp edge separation, and a soft, natural contact shadow on the floor. "
        f"Camera perspective: {perspective}, shot on 85mm commercial lens, tack-sharp edge-to-edge focus, zero clutter, no people, no hands, no 2D text overlays or graphic banners superimposed on the image. "
        f"Composition: Elegant vertical portrait product showcase, 8k resolution, ultra-clean commercial advertising aesthetic, photorealistic."
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt,
    )

    image_bytes = None
    mime_type = "image/jpeg"
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            image_bytes = part.inline_data.data
            mime_type = part.inline_data.mime_type or "image/jpeg"
            break

    if not image_bytes:
        raise RuntimeError("No image returned from gemini-3.1-flash-lite-image")

    # Upload to Cloud Storage
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    ext = "png" if "png" in mime_type else "jpg"
    filename = f"swag/{uuid.uuid4().hex[:12]}_{company_name.lower().replace(' ', '_')}.{ext}"
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    return public_url
