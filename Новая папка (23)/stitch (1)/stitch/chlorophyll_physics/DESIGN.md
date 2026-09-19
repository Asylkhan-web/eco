# Design System Strategy: The Symbiotic Laboratory

## 1. Overview & Creative North Star
**Creative North Star: "Organic Precision"**
This design system moves away from the sterile, rigid grids of traditional educational software. Instead, it treats the interface as a living ecosystem where the mathematical rigor of Physics meets the fluid grace of Nature. We avoid "template-style" layouts by embracing **intentional asymmetry** and **tonal depth**.

The system breaks the standard "box-within-a-box" look by using overlapping elements—such as a leaf illustration subtly breaking the frame of a physics diagram—and editorial typography scales that favor breathing room over information density. The goal is a digital environment that feels as calming as a botanical garden but as structured as a laboratory.

## 2. Color & Surface Philosophy
The palette is rooted in a "Soil to Sky" philosophy, using the provided Material Design tokens to create a sophisticated, layered environment.

*   **The "No-Line" Rule:** Standard 1px borders are strictly prohibited for sectioning. Boundaries must be defined through background shifts. For example, a `surface-container-low` side navigation sitting against a `surface` main content area provides all the separation necessary without the visual noise of a line.
*   **Surface Hierarchy & Nesting:** Treat the UI as physical layers of fine vellum. 
    *   **Level 0 (Base):** `surface` (#f0fdf1)
    *   **Level 1 (Sectioning):** `surface-container-low` (#eaf7eb)
    *   **Level 2 (Cards/Interaction):** `surface-container-lowest` (#ffffff)
*   **The "Glass & Gradient" Rule:** To reflect the "Science" aspect, use Glassmorphism for floating panels (e.g., progress trackers). Apply a `backdrop-blur` of 12px to a 60% opaque `surface-container-lowest`.
*   **Signature Textures:** For high-impact elements like "Eco-Coin" balances or "Module Complete" states, use a subtle linear gradient from `primary` (#0d631b) to `primary-container` (#2e7d32). This creates a "silky" finish that feels premium and custom.

## 3. Typography
We use a high-contrast pairing to distinguish between academic data and storytelling.

*   **Display & Headlines (Space Grotesk):** This typeface brings a mathematical, "engineered" feel. Use `display-lg` and `headline-md` for unit titles and major milestones. The wide apertures of Space Grotesk mirror the openness of the nature theme.
*   **Body & Labels (Inter):** Inter is our workhorse for legibility. Its neutral, modern tone ensures that complex physics equations and long-form reading remain accessible.
*   **Identity through Scale:** Use `display-lg` sparingly to create "editorial moments." A large, light-weight header next to a small, dense "Eco-Point" badge creates a sophisticated, non-traditional hierarchy.

## 4. Elevation & Depth
Depth in this system is achieved through **Tonal Layering** and light physics, not artificial structure.

*   **The Layering Principle:** Avoid shadows for static content. Place a `surface-container-lowest` card on a `surface-container-low` background to create a "soft lift."
*   **Ambient Shadows:** For active elements (hovered cards, modals), use "Naturalist Shadows." These must be ultra-diffused: `box-shadow: 0 20px 40px rgba(19, 30, 23, 0.05)`. Note the use of the `on-surface` color (#131e17) for the shadow tint rather than pure black, ensuring the shadow feels like it’s cast by leaves, not lead.
*   **The "Ghost Border" Fallback:** If a border is required for high-accessibility contexts, use `outline-variant` at 20% opacity. Never use 100% opaque outlines.
*   **Glassmorphism:** Use semi-transparent layers for "Physics Overlays" (e.g., a diagram appearing over a nature photo). This integrates the scientific data into the environment rather than "pasting" it on top.

## 5. Component Guidelines

### Buttons & Actions
*   **Primary Action:** Forest Green (`primary`). Use `rounded-xl` (1.5rem) for a friendly, organic feel. No sharp corners.
*   **Secondary/Coins:** Warm Amber (`tertiary`). These should feature a slight `surface-tint` to give "Eco-Coins" a metallic yet earthy glow.
*   **Tertiary:** Text-only with an underline that appears on hover, using the `primary` color.

### Progress & Gamification
*   **Eco-Progress Bars:** Use a thick `primary-fixed` track with a `primary` fill. The "cap" of the progress bar should be an organic shape, like a small leaf or atom symbol.
*   **Knowledge Points:** Displayed in `tertiary-container` chips with `rounded-full` corners.

### Cards & Lists
*   **Forbidden:** Divider lines between list items.
*   **Requirement:** Use 24px (1.5rem) of vertical whitespace between list items. For complex lists, alternate the background color of the items between `surface` and `surface-container-low`.

### Input Fields
*   **Styling:** Use the "Pill" shape (`rounded-full`). The fill should be `surface-container-highest` with no border. On focus, transition to a `surface-container-lowest` fill with a subtle 1px `primary` ghost border (20% opacity).

## 6. Do's and Don'ts

### Do
*   **DO** use whitespace as a functional tool. If a screen feels crowded, increase the spacing rather than adding lines.
*   **DO** mix physics diagrams with organic photography. A black-and-white photo of a forest with a neon `primary` vector of a gravitational wave overlaid is the core aesthetic.
*   **DO** use `surface-bright` for areas meant to inspire focus, like the actual lesson content.

### Don't
*   **DON'T** use pure black (#000000) for text. Always use `on-surface` (#131e17) to maintain the organic, soft-contrast feel.
*   **DON'T** use "Standard" Material Design shadows. They are too heavy for this "Light & Airy" theme.
*   **DON'T** use sharp `none` or `sm` roundedness. Everything in nature has a radius; our UI should too. Stick to `md` (0.75rem) or higher.