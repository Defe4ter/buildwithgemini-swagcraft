# My agent: SwagCraft (Company Swag Studio & Product Showcase)

One-liner: A conversational agent that helps companies and teams discover their latest brand milestones and generates a clean product showcase of customized company swag (hoodies, steel bottles, socks, stickers, etc.) with Nano Banana 2 generated visuals.

Tool coverage:
- Memory: Remembers the user's company name, brand style/aesthetic, previously generated swag items, and user preferences (e.g. minimalist, bold, eco-friendly).
- Tools:
  - Search tool (Google Search grounding / web lookup) to find the latest updates, achievements, mission, or aesthetic of the target company.
  - Image generation tool (`gemini-3.1-flash-lite-image` / Nano Banana 2 Lite) to generate a realistic product mockup photo with the company's brand, colors, and recent achievements reflected on the chosen swag item.
  - Storage tool / GCS upload to host the generated swag image publicly so it renders in the UI.
  - Random swag picker ("Surprise Me" selection logic with expanded swag catalog: tumblers, totes, enamel pins, desk mats, wireless chargers, etc.).
- Catalog/UI: A2UI rich product card featuring the swag item title, celebration milestone/tagline, description, and the rendered product mockup image underneath.
- Image gen: Generates crisp product mockups (e.g. steel water bottle, hoodie, socks, laptop stickers, tote bag) using `gemini-3.1-flash-lite-image` (Nano Banana 2).
- Sandbox: n/a (or optional for bulk pricing / batch order cost calculation if desired).

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits):
- Expanded merchandise item catalog with randomizer for "Surprise Me" mode
- Swag package cost estimator (code sandbox / math calculation)
- Exportable swag kit summary / order card
