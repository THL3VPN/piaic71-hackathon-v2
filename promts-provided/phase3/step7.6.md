# specs.md

## Step 7.6: Chat UI Usability & Visual Polish (ChatGPT-Style Widget)

### Objective
Improve the existing chat widget UI to be **highly user-friendly, clean, and visually consistent**, inspired by the ChatGPT chat experience.  
This step focuses purely on **UI/UX polish and response conciseness**, without changing backend behavior or API contracts.

---

## Problem Statement
The current chat UI is functional but:
- Feels visually unbalanced and inconsistent
- Is not optimized for readability or ease of use
- Does not resemble familiar modern chat interfaces
- Produces overly verbose responses in some cases

This step addresses those gaps.

---

## In Scope
- UI layout and styling improvements using **Tailwind CSS**
- Chat widget layout refinements (spacing, alignment, sizing)
- Input/composer UX improvements
- Message bubble styling
- Minor agent prompt tuning for concise responses

## Out of Scope
- Backend API changes
- New endpoints or models
- Streaming responses
- Business logic changes
- Task or conversation behavior changes

---

## Design & UX Requirements

### 1) Overall Look & Feel
- The chat widget MUST visually resemble the **ChatGPT chat interface**:
  - Clean
  - Minimal
  - Content-focused
- Use Tailwind CSS utility classes for layout, spacing, and typography.
- Prefer neutral colors (gray/white) with subtle accent colors.

---

### 2) Layout & Responsiveness
- The chat widget MUST:
  - Fit fully within the viewport
  - Never introduce **horizontal scrolling**
  - Be responsive on common laptop screen sizes

Rules:
- `overflow-x` MUST be disabled or avoided
- Message content MUST wrap naturally
- Containers MUST use max-width constraints and padding

---

### 3) Typography & Alignment
- All visible text (header, messages, placeholders, buttons) MUST:
  - Be visually symmetrical
  - Use consistent font sizes for similar elements
  - Follow a clear hierarchy:
    - Header/title
    - Message text
    - Metadata (timestamps, optional)

Guidelines:
- Header text size: slightly larger and bold
- Message text size: normal, readable
- Avoid mixing inconsistent font sizes

---

### 4) Chat Header
- Title: “Todo Assistant”
- Centered or left-aligned consistently
- Font size and weight MUST match the rest of the UI
- Close button aligned cleanly (no overlap or misalignment)

---

### 5) Message List (Chat Body)
- Messages MUST appear as chat bubbles:
  - User messages aligned right
  - Assistant messages aligned left
- Bubble styling:
  - Rounded corners
  - Comfortable padding
  - Soft background colors
- Spacing between messages MUST be consistent
- Auto-scroll to latest message MUST work smoothly

---

### 6) Composer / Input Area (Critical UX)
- The text input MUST:
  - Always be visible (never scroll out of view)
  - Be fixed to the bottom of the chat panel
- The send button MUST:
  - Be a **small circular button**
  - Appear at the right side of the input
  - Use an icon (e.g. arrow or send icon)
- Enter key MUST send the message

Layout rules:
- Input and send button MUST be on the same row
- Input expands horizontally
- Button does NOT consume excessive space

---

### 7) No Horizontal Scroll Guarantee
The following MUST be enforced:
- No element causes overflow beyond container width
- Long words or responses MUST wrap
- Tool/debug info (if shown) MUST be collapsible and wrapped

---

### 8) Clean & Minimal Presentation
- Avoid clutter:
  - No unnecessary borders
  - No excessive colors
  - No dense text blocks
- White space MUST be used intentionally for readability
- Animations (if any) MUST be subtle (fade/slide)

---

## Response Conciseness Requirement (Assistant Tone)

### Objective
Ensure assistant responses are **specific, precise, and concise**.

Guidelines:
- Prefer one-word or two-word answers where sufficient
- Avoid unnecessary explanations
- Confirm actions briefly:
  - “Added.”
  - “Done.”
  - “Updated.”
  - “Deleted.”
- Lists should be short and readable

Backend note (optional, allowed):
- Agent system prompt MAY be lightly tuned to emphasize:
  - “Be concise.”
  - “Avoid verbosity.”
- No change to logic or tool usage is allowed.

---

## Accessibility & Usability
- Input auto-focus when widget opens
- Clear focus states for keyboard navigation
- Buttons must have sufficient contrast
- Click/tap targets must be comfortable

---

## Acceptance Criteria

UI & Layout
- [ ] Chat widget fits fully in viewport with no horizontal scrolling
- [ ] Typography is consistent and symmetrical
- [ ] Layout visually resembles ChatGPT-style chat

Composer
- [ ] Input is always visible
- [ ] Send button is circular and aligned to the right
- [ ] Enter key sends message

Messages
- [ ] Chat bubbles are clean and readable
- [ ] Proper alignment (user vs assistant)
- [ ] Auto-scroll works reliably

User Experience
- [ ] UI feels neat, clean, and easy to use
- [ ] Assistant responses are short and precise
- [ ] No visual clutter or layout breakage

---

## Step Exit Criteria
This step is complete when:
- Chat UI feels polished and intuitive
- Layout issues and scrolling problems are resolved
- The widget matches modern chat UX expectations
- Assistant responses are concise and user-friendly
- No backend or functional regressions are introduced
