# Research Brief: MDN Canvas API requestAnimationFrame

## Status
complete

## Query
MDN Canvas API requestAnimationFrame

## Reason
None

## Sources

| Title | URL | Status | Retrieved | Notes |
|---|---|---|---|---|
| Window: requestAnimationFrame() method - MDN | https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame | fetched | 2026-05-09T12:50:00 | Primary API reference |
| Basic animations - MDN | https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations | fetched | 2026-05-09T12:51:00 | Implementation guide |

## Extracted Findings

- **Purpose**: `requestAnimationFrame()` tells the browser you wish to perform an animation and requests a callback before the next repaint.
- **Efficiency**: Pauses automatically in background tabs, saving CPU and battery.
- **Frame Rate**: Callback frequency usually matches display refresh rate (e.g. 60Hz).
- **Animation Loop**: Recommended steps for canvas: clear, save state, draw, restore state.
- **Synchronization**: Preferred over `setInterval` for smooth, flicker-free animations.

## Copyright / Safety Notes
Extracted from public web sources using local browser automation. No prohibited IP terms detected in summary.

## Technical Notes
- Backend: playwright
- Timestamp: 2026-05-09T17:49:00.000000
