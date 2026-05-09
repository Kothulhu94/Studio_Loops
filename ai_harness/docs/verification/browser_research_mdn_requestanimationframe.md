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
| Canvas API - Web APIs | MDN | https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API | fetched | 2026-05-09T13:20:40.321657 |  |
| VRDisplay: requestAnimationFrame() method - Web APIs | MDN | https://developer.mozilla.org/en-US/docs/Web/API/VRDisplay/requestAnimationFrame | fetched | 2026-05-09T13:20:42.098278 |  |
| XRSession: requestAnimationFrame() method - Web APIs | MDN | https://developer.mozilla.org/en-US/docs/Web/API/XRSession/requestAnimationFrame | fetched | 2026-05-09T13:20:44.154755 |  |

## Extracted Findings

### Finding
Canvas API - Web APIs | MDN <meta name="description" content="The Canvas API provides a means for drawing graphics via JavaScript and the HTML element. Among other things, it can be used for animation, game graphics, data visualization, photo manipulation, and real-time video processing."><meta name="og:description" content="The Canvas API provides a means for drawing graphics via JavaScript and the HTML element. Among other things, it can be used for animation, game graphics, data visualization, photo manipulation, and real-time video processing."> Skip to main content Skip to search Web Web APIs Canvas API Canvas API Baseline Widely available This feature is well established and works across many devices and browser versions. It’s been available across browsers since July 2015. Learn more See full compatibility Report feedback The Canvas API provides a means for drawing graphics via JavaScript and the HTML element. Among other things, it can be used for animation, game graphics, data visualization, photo manipulation, and real-time video processing. The Canvas API largely focuses on 2D graphics. The WebGL API, which also uses the element, draws hardware-accelerated 2D and 3D graphics. Basic example This simple example draws a green rectangle onto a canvas. HTML JavaScript The Document.getElementById() method gets a reference to the HTML element. Next, the HTMLCanvasElement.getContext() method gets that element's context—the thing onto which the drawing will be rendered. The actual drawing is done using the CanvasRenderingContext2D interface. The fillStyle property makes the rectangle green. The fillRect() method places its top-left corner at (10, 10), and gives it a size of 150 units wide by 100 tall. Result Reference HTMLCanvasElement CanvasRenderingContext2D CanvasGradient CanvasPattern ImageBitmap ImageData TextMetrics OffscreenCanvas Path2D ImageBitmapRenderingContext Note: The interfaces related to the WebGLRenderingContext are referenced under WebGL. Note: O

### Finding
VRDisplay: requestAnimationFrame() method - Web APIs | MDN Skip to main content Skip to search Web Web APIs VRDisplay requestAnimationFrame() VRDisplay: requestAnimationFrame() method Deprecated: This feature is no longer recommended. Though some browsers might still support it, it may have already been removed from the relevant web standards, may be in the process of being dropped, or may only be kept for compatibility purposes. Avoid using it, and update existing code if possible; see the compatibility table at the bottom of this page to guide your decision. Be aware that this feature may cease to work at any time. Non-standard: This feature is not standardized. We do not recommend using non-standard features in production, as they have limited browser support, and may change or be removed. However, they can be a suitable alternative in specific cases where no standard option exists. The requestAnimationFrame() method of the VRDisplay interface is a special implementation of Window.requestAnimationFrame containing a callback function that will be called every time a new frame of the VRDisplay presentation is rendered: Note: This method was part of the old WebVR API. It has been superseded by the WebXR Device API. When the VRDisplay is not presenting a scene, this is functionally equivalent to Window.requestAnimationFrame. When the VRDisplay is presenting, the callback is called at its native refresh rate. Syntax Parameters callback A callback function that will be called every time a new frame of the VRDisplay presentation is rendered. Return value A long representing the handle of the requestAnimationFrame() call. This can then be passed to a VRDisplay.cancelAnimationFrame() call to unregister the callback. Examples Note: You can see this complete code at raw-webgl-example. Specifications This method was part of the old WebVR API that has been superseded by the WebXR Device API. It is no longer on track to becoming a standard. Until all browsers have implemented 

### Finding
XRSession: requestAnimationFrame() method - Web APIs | MDN Skip to main content Skip to search Web Web APIs XRSession requestAnimationFrame() XRSession: requestAnimationFrame() method Limited availability This feature is not Baseline because it does not work in some of the most widely-used browsers. Learn more See full compatibility Report feedback Experimental: This is an experimental technologyCheck the Browser compatibility table carefully before using this in production. Secure context: This feature is available only in secure contexts (HTTPS), in some or all supporting browsers. The XRSession method requestAnimationFrame(), much like the Window method of the same name, schedules a callback to be executed the next time the browser is ready to paint the session's virtual environment to the XR display. The specified callback is executed once before the next repaint; if you wish for it to be executed for the following repaint, you must call requestAnimationFrame() again. This can be done from within the callback itself. The callback takes two parameters as inputs: an XRFrame describing the state of all tracked objects for the session, and a timestamp you can use to compute any animation updates needed. You can cancel a previously scheduled animation by calling cancelAnimationFrame(). Note: Despite the obvious similarities between these methods and the global requestAnimationFrame() function provided by the Window interface, you must not treat these as interchangeable. There is no guarantee that the latter will work at all while an immersive XR session is underway. Syntax Parameters animationFrameCallback A function which is called before the next repaint in order to allow you to update and render the XR scene based on elapsed time, animation, user input changes, and so forth. The callback receives as input two parameters: time A DOMHighResTimeStamp indicating the time offset at which the updated viewer state was received from the WebXR device. xrFrame An XRFrame ob


## Copyright / Safety Notes
Extracted from public web sources using local browser automation. No prohibited IP terms detected in summary.

## Technical Notes
- Backend: playwright
- Timestamp: 2026-05-09T13:20:44.163872
