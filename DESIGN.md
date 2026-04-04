# Design System Document

## 1. Overview & Creative North Star: "The Precision Architect"

This design system is engineered to transform complex stochastic data into a high-end, editorial-grade experience. The Creative North Star, **"The Precision Architect,"** balances the heavy technicality of oil resource modeling with an airy, sophisticated interface that feels both authoritative and effortless.

To move beyond the "standard SaaS" look, we employ a philosophy of **Tonal Depth**. This means breaking the rigid grid through intentional asymmetry, overlapping layers that mimic stacked physical sheets of glass, and a high-contrast typographic scale that treats data as a narrative rather than a spreadsheet. The result is a UI that doesn't just display information—it curates it.

---

## 2. Colors: Depth Through Atmosphere

Our palette is rooted in the deep, metallic blues and slates of the STORM identity, contrasted against "Electric Cyan" for technical precision.

### The "No-Line" Rule
**Explicit Instruction:** You are prohibited from using 1px solid borders to define sections. Layout boundaries must be established exclusively through background color shifts. For example, a `surface-container-low` section should sit on a `surface` background. Containment is an atmospheric effect, not a structural one.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. We use the surface tiers to define depth:
- **`surface-container-lowest` (#ffffff):** Used for primary cards or floating data panels to provide maximum lift.
- **`surface-container-low` (#f2f4f6):** The standard background for secondary content areas.
- **`surface` (#f7f9fb):** The global canvas.
- **`surface-container-highest` (#e0e3e5):** Reserved for deep-inset elements like search bars or navigation foundations.

### The "Glass & Gradient" Rule
Floating elements (modals, popovers) should utilize **Glassmorphism**. Apply a semi-transparent `surface` color with a `backdrop-filter: blur(20px)`. To add "soul" to the technical aesthetic, use subtle linear gradients (e.g., `primary` to `primary-container`) for CTAs, mimicking the metallic sheen found in the STORM logo.

---

## 3. Typography: Editorial Authority

We pair **Space Grotesk** for high-impact display moments with **Inter** for technical readability. This combination signals a bridge between innovative modeling and reliable data.

- **Display & Headlines (Space Grotesk):** Large, bold, and slightly wide. Use `display-lg` (3.5rem) to anchor dashboard overviews. The geometric nature of Space Grotesk echoes the industrial lightning and bar elements of the logo.
- **Body & Labels (Inter):** Optimized for the dense numerical data required by the Stochastic Oil Resource Model. Inter’s tall x-height ensures that complex figures are legible even at `body-sm` (0.75rem).
- **Hierarchy as Identity:** Use drastic scale shifts. A `headline-lg` title next to a `label-sm` technical metric creates an editorial "pull" that guides the eye toward the most critical decision points.

---

## 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are often a crutch for poor spacing. In this system, depth is earned through tone and ambient light.

- **The Layering Principle:** Stack your containers. A `surface-container-lowest` card placed atop a `surface-container-low` section creates a soft, natural lift without a single pixel of shadow.
- **Ambient Shadows:** When a "floating" effect is mandatory (e.g., a critical Alert Modal), use extra-diffused shadows. 
  - **Token:** `box-shadow: 0 12px 40px rgba(25, 28, 30, 0.06);` 
  - Note the low opacity (6%) and large blur—this mimics natural light rather than a digital drop shadow.
- **The "Ghost Border" Fallback:** If a container lacks sufficient contrast against its background, use a "Ghost Border": `outline-variant` (#c3c7ce) at **15% opacity**. Never use 100% opaque borders.

---

## 5. Components: Technical Elegance

### Buttons
- **Primary:** A subtle gradient from `primary` (#012743) to `primary_container` (#1d3d5a). Rounded corners at `DEFAULT` (0.5rem).
- **Secondary:** Transparent background with a `Ghost Border`. Text in `primary`.
- **Tertiary:** Purely typographic, using `label-md` with a slight `letter-spacing` increase for a premium feel.

### Data Grids & Lists
- **The "No Divider" Rule:** Forbid the use of horizontal lines between list items. Instead, use vertical white space (Spacing `3` or `4`) and subtle background hover states (`surface_container_high`).
- **Dynamic Grids:** Use `surface-container-lowest` for individual cell blocks in a grid to create a "bento box" feel that organizes complex oil resource variables into digestible clusters.

### Input Fields & Forms
- **Modern Wells:** Inputs should be styled as "wells"—using `surface-container-highest` with a `sm` (0.25rem) rounded corner. 
- **Active State:** Focus is indicated by a 2px `tertiary_fixed_dim` (Electric Cyan) bottom border only, maintaining the "Precision Architect" aesthetic.

### Additional Signature Components
- **Stochastic Status Chips:** High-contrast `tertiary_container` for positive data ("Pass") and `error_container` for alerts. Use lowercase `label-md` to maintain a modern, technical tone.
- **Glass Navigation:** A split-panel sidebar using `surface-container-low` with a `backdrop-filter: blur(10px)`.

---

## 6. Do's and Don'ts

### Do
- **Do** use generous margins (Spacing `8` or `10`) between unrelated data modules to reduce cognitive load.
- **Do** use the `Electric Cyan` (`tertiary_fixed_dim`) sparingly as a "laser pointer" to highlight the most important data point on a screen.
- **Do** lean into asymmetry; allow a right-hand data panel to be wider than the left-hand navigation to create a sense of focused workspace.

### Don't
- **Don't** use 1px solid black or dark grey borders. This immediately "cheapens" the technical look.
- **Don't** use standard "Material Design" blue. Stick to the signature `primary` (#012743) extracted from the STORM logo for brand authority.
- **Don't** crowd the screen. If a data grid feels tight, increase the spacing tokens rather than shrinking the font size. Readability is the priority.