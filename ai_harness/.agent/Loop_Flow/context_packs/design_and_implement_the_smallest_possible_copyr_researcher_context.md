# Context Pack: design_and_implement_the_smallest_possible_copyr / researcher

## Feature Goal
Design and implement the smallest possible copyright-safe sci-fi base management prototype slice: room placement data model, worker task queue, and one simple Vitest test. Keep scope tiny. Do not add UI. Do not add dependencies.

## Current Stage
researcher

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/design_and_implement_the_smallest_possible_copyr_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{}

## Relevant Research Briefs
### design_and_implement_the_smallest_possible_copyr_researcher_Analyze_the_existing_TypeScrip_research_brief.md
# Research Brief: Analyze the existing TypeScript codebase to map the specific interfaces for StateStore and PromptCompiler.

## Status
complete

## Query
Analyze the existing TypeScript codebase to map the specific interfaces for StateStore and PromptCompiler.

## Reason
None

## Sources

| Title | URL | Status | Retrieved | Notes |
|---|---|---|---|---|
| TypeScript: Documentation - Everyday Types | https://www.typescriptlang.org/docs/handbook/2/everyday-types.html | fetched | 2026-05-09T21:33:01.491269 | coverage: typescript, javascript data structures, testing/vitest |
| Unknown Title | https://www.typescriptlang.org/docs/handbook/2/objects.html | fetched | 2026-05-09T21:33:03.165112 | coverage: typescript, javascript data structures, query:specific, query:typescript |
| Getting Started \| Guide \| Vitest | https://vitest.dev/guide | fetched | 2026-05-09T21:33:06.468696 | coverage: animation/rendering, javascript data structures, browser/runtime, testing/vitest |
| Test \| Vitest | https://vitest.dev/api | fetched | 2026-05-09T21:33:08.098795 | coverage: javascript data structures, testing/vitest |
| Array - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array | fetched | 2026-05-09T21:33:09.573702 | coverage: javascript data structures, browser/runtime |
| Map - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map | fetched | 2026-05-09T21:33:12.547125 | coverage: javascript data structures, browser/runtime |
| File System API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/File_System_API | fetched | 2026-05-09T21:33:14.006246 | coverage: typescript, queue/task scheduling, browser/runtime, query:interfaces, query:specific |
| Fetch API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API | fetched | 2026-05-09T21:33:15.798523 | coverage: typescript, javascript data structures, queue/task scheduling, browser/runtime |

## Extracted Findings

### Finding
TypeScript: Documentation - Everyday TypesSkip to main contentTypeScriptin EnWas this page helpful?Everyday TypesIn this chapter, we'll cover some of the most common types of values you'll find in JavaScript code, and explain the corresponding ways to describe those types in TypeScript. This isn't an exhaustive list, and future chapters will describe more ways to name and use other types. Types can also appear in many more places than just type annotations. As we learn about the types themselves, we'll also learn about the places where we can refer to these types to form new constructs. We'll start by reviewing the most basic and common types you might encounter when writing JavaScript or TypeScript code. These will later form the core building blocks of more complex types. The primitives: string, number, and boolean JavaScript has three very commonly used primitives: string, number, and boolean. Each has a corresponding type in TypeScript. As you might expect, these are the same names you'd see if you used the JavaScript typeof operator on a value of those types: string represents string values like "Hello, world" number is for numbers like 42. JavaScript does not have a special runtime value for integers, so there's no equivalent to int or float - everything is simply number boolean is for the two values true and false The type names String, Number, and Boolean (starting with capital letters) are legal, but refer to some special built-in types that will very rarely appear in your code. Always use string, number, or boolean for types. Arrays To specify the type of an array like [1, 2, 3], you can use the syntax number[]; this syntax works for any type (e.g. string[] is an array of strings, and so on). You may also see this written as Array, which means the same thing. We'll learn more about the syntax T when we cover generics. Note that [number] is a different thing; refer to the section on Tuples. any TypeScript also has a special type, any, that you can use whene

### Finding


### design_and_implement_the_smallest_possible_copyr_researcher_Investigate_the_current_Vitest_research_brief.md
# Research Brief: Investigate the current Vitest configuration to ensure compatibility with the proposed orchestration lifecycle testing.

## Status
complete

## Query
Investigate the current Vitest configuration to ensure compatibility with the proposed orchestration lifecycle testing.

## Reason
None

## Sources

| Title | URL | Status | Retrieved | Notes |
|---|---|---|---|---|
| TypeScript: Documentation - Everyday Types | https://www.typescriptlang.org/docs/handbook/2/everyday-types.html | fetched | 2026-05-09T21:33:41.793246 | coverage: typescript, javascript data structures, testing/vitest |
| TypeScript: Documentation - Object Types | https://www.typescriptlang.org/docs/handbook/2/objects.html | fetched | 2026-05-09T21:33:43.609126 | coverage: typescript, javascript data structures |
| Getting Started \| Guide \| Vitest | https://vitest.dev/guide | fetched | 2026-05-09T21:33:45.140143 | coverage: animation/rendering, javascript data structures, browser/runtime, testing/vitest, query:testing, query:vitest |
| Test \| Vitest | https://vitest.dev/api | fetched | 2026-05-09T21:33:46.741714 | coverage: javascript data structures, testing/vitest, query:current, query:vitest |
| Array - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array | fetched | 2026-05-09T21:33:48.391341 | coverage: javascript data structures, browser/runtime |
| Map - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map | fetched | 2026-05-09T21:33:50.343644 | coverage: javascript data structures, browser/runtime |
| File System API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/File_System_API | fetched | 2026-05-09T21:33:51.791986 | coverage: typescript, queue/task scheduling, browser/runtime |
| Fetch API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API | fetched | 2026-05-09T21:33:53.265656 | coverage: typescript, javascript data structures, queue/task scheduling, browser/runtime |

## Extracted Findings

### Finding
TypeScript: Documentation - Everyday TypesSkip to main contentTypeScriptin EnWas this page helpful?Everyday TypesIn this chapter, we'll cover some of the most common types of values you'll find in JavaScript code, and explain the corresponding ways to describe those types in TypeScript. This isn't an exhaustive list, and future chapters will describe more ways to name and use other types. Types can also appear in many more places than just type annotations. As we learn about the types themselves, we'll also learn about the places where we can refer to these types to form new constructs. We'll start by reviewing the most basic and common types you might encounter when writing JavaScript or TypeScript code. These will later form the core building blocks of more complex types. The primitives: string, number, and boolean JavaScript has three very commonly used primitives: string, number, and boolean. Each has a corresponding type in TypeScript. As you might expect, these are the same names you'd see if you used the JavaScript typeof operator on a value of those types: string represents string values like "Hello, world" number is for numbers like 42. JavaScript does not have a special runtime value for integers, so there's no equivalent to int or float - everything is simply number boolean is for the two values true and false The type names String, Number, and Boolean (starting with capital letters) are legal, but refer to some special built-in types that will very rarely appear in your code. Always use string, number, or boolean for types. Arrays To specify the type of an array like [1, 2, 3], you can use the syntax number[]; this syntax works for any type (e.g. string[] is an array of strings, and so on). You may also see this written as Array, which means the same thing. We'll learn more about the syntax T when we cover generics. Note that [number] is a different thing; refer to the section on Tuples. any TypeScript also has a special type, any, that you can use whene

### Finding


### design_and_implement_the_smallest_possible_copyr_researcher_Examine_the__agent_workflows_research_brief.md
# Research Brief: Examine the .agent/workflows/ directory to understand the schema requirements for TypeScript-based workflows.

## Status
complete

## Query
Examine the .agent/workflows/ directory to understand the schema requirements for TypeScript-based workflows.

## Reason
None

## Sources

| Title | URL | Status | Retrieved | Notes |
|---|---|---|---|---|
| TypeScript: Documentation - Everyday Types | https://www.typescriptlang.org/docs/handbook/2/everyday-types.html | fetched | 2026-05-09T21:34:21.275116 | coverage: typescript, javascript data structures, testing/vitest |
| TypeScript: Documentation - Object Types | https://www.typescriptlang.org/docs/handbook/2/objects.html | fetched | 2026-05-09T21:34:23.022330 | coverage: typescript, javascript data structures |
| Array - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array | fetched | 2026-05-09T21:34:24.700267 | coverage: javascript data structures, browser/runtime |
| Map - JavaScript \| MDN | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map | fetched | 2026-05-09T21:34:26.520366 | coverage: javascript data structures, browser/runtime |
| File System API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/File_System_API | fetched | 2026-05-09T21:34:28.174804 | coverage: typescript, queue/task scheduling, browser/runtime |
| Fetch API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API | fetched | 2026-05-09T21:34:29.808130 | coverage: typescript, javascript data structures, queue/task scheduling, browser/runtime |
| Geolocation API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API | fetched | 2026-05-09T21:34:32.062049 | coverage: javascript data structures, browser/runtime |
| HTML DOM API - Web APIs \| MDN | https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API | fetched | 2026-05-09T21:34:34.106680 | coverage: typescript, javascript data structures, queue/task scheduling, browser/runtime, testing/vitest, state/modeling |

## Extracted Findings

### Finding
TypeScript: Documentation - Everyday TypesSkip to main contentTypeScriptin EnWas this page helpful?Everyday TypesIn this chapter, we'll cover some of the most common types of values you'll find in JavaScript code, and explain the corresponding ways to describe those types in TypeScript. This isn't an exhaustive list, and future chapters will describe more ways to name and use other types. Types can also appear in many more places than just type annotations. As we learn about the types themselves, we'll also learn about the places where we can refer to these types to form new constructs. We'll start by reviewing the most basic and common types you might encounter when writing JavaScript or TypeScript code. These will later form the core building blocks of more complex types. The primitives: string, number, and boolean JavaScript has three very commonly used primitives: string, number, and boolean. Each has a corresponding type in TypeScript. As you might expect, these are the same names you'd see if you used the JavaScript typeof operator on a value of those types: string represents string values like "Hello, world" number is for numbers like 42. JavaScript does not have a special runtime value for integers, so there's no equivalent to int or float - everything is simply number boolean is for the two values true and false The type names String, Number, and Boolean (starting with capital letters) are legal, but refer to some special built-in types that will very rarely appear in your code. Always use string, number, or boolean for types. Arrays To specify the type of an array like [1, 2, 3], you can use the syntax number[]; this syntax works for any type (e.g. string[] is an array of strings, and so on). You may also see this written as Array, which means the same thing. We'll learn more about the syntax T when we cover generics. Note that [number] is a different thing; refer to the section on Tuples. any TypeScript also has a special type, any, that you can use whene

### Finding




## Validation Status
[]

## Pruned Source Context
--- Context Pruning Map for: ['design', 'implement', 'smallest', 'possible', 'copyright-safe', 'sci-fi', 'base', 'management', 'prototype', 'slice:', 'room', 'placement', 'data', 'researcher', 'design_and_implement_the_smallest_possible_copyr_researcher_investigate_the_current_vitest_research_brief.md', 'design_and_implement_the_smallest_possible_copyr_researcher_examine_the__agent_workflows_research_brief.md', 'investigate', 'current', 'vitest', 'configuration'] ---
ai_harness_bundle.txt: L1379-L1398, L1676-L1695, L547-L566, L555-L574, L44-L63
HANDOFF_SCHEMA.json: L62-L81, L41-L60, L47-L66, L57-L76, L34-L53
package-lock.json: L1200-L1219, L1206-L1225, L1254-L1273, L485-L504, L515-L534
package.json: L7-L14, L3-L14
tsconfig.json: L8-L14, L6-L14
vitest.config.ts: L1-L8
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L15-L34, L37-L56, L56-L75, L24-L43
.agent/bin/licenses/github.com/atotto/clipboard/LICENSE: L19-L27
.agent/bin/licenses/github.com/fsnotify/fsnotify/LICENSE: L17-L25
.agent/bin/licenses/github.com/godbus/dbus/v5/LICENSE: L16-L25
.agent/bin/licenses/github.com/gorilla/css/scanner/LICENSE: L19-L28
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/CHANGELOG.md: L1-L18
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L322-L341, L188-L207, L109-L128, L93-L112, L18-L37
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither_test.go: L177-L196, L178-L197
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/draw.go: L40-L59, L7-L26, L123-L142, L8-L27, L1-L17
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/error_diffusers.go: L2-L21, L26-L45, L5-L24, L7-L26, L14-L33
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L76-L95, L357-L373, L40-L59, L220-L239, L217-L236
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/pixelmappers.go: L183-L202, L310-L329, L172-L191, L188-L207, L109-L128
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L1-L20, L25-L44, L148-L167
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/special.go: L2-L9
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/examples/gif_image/main.go: L1-L17
.agent/bin/licenses/github.com/microcosm-cc/bluemonday/LICENSE.md: L20-L28
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L15-L34, L37-L56, L56-L75, L24-L43
.agent/bin/licenses/github.com/minio/selfupdate/internal/osext/LICENSE: L19-L27
.agent/bin/licenses/github.com/pkg/browser/LICENSE: L15-L23
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L55-L74, L23-L42, L14-L33, L36-L55
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L55-L74, L23-L42, L14-L33, L36-L55
.agent/bin/licenses/github.com/spf13/pflag/LICENSE: L20-L28
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L15-L34, L37-L56, L56-L75, L24-L43
.agent/bin/licenses/golang.org/x/crypto/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/image/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/mod/semver/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/net/html/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/oauth2/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sync/errgroup/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sys/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/term/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/text/LICENSE: L19-L27
.agent/Loop_Flow/autonomous_studio_expansion_blueprint.md: L12-L17, L9-L17, L10-L17, L11-L17
.agent/Loop_Flow/source_index.json: L523-L542, L451-L470, L4-L23, L571-L590, L553-L572
.agent/orchestrator/actions_schema.json: L87-L106, L7-L26, L8-L27
.agent/orchestrator/artifact_store.py: L3-L22, L13-L32, L10-L29
.agent/orchestrator/artifact_validator.py: L1-L20, L2-L21, L26-L45, L152-L171, L184-L203
.agent/orchestrator/browser_research.py: L194-L213, L63-L82, L70-L89, L53-L72, L105-L124
.agent/orchestrator/capability_registry.py: L71-L90, L74-L93, L97-L116, L107-L126, L66-L85
.agent/orchestrator/command_allowlist.json: L12-L31, L6-L25
.agent/orchestrator/command_runner.py: L69-L88
.agent/orchestrator/config.json: L1-L17
.agent/orchestrator/context_compactor.py: L43-L62
.agent/orchestrator/context_pruner.py: L113-L126, L65-L84, L61-L80, L28-L47, L19-L38
.agent/orchestrator/copyright_guard.py: L1-L20, L47-L66, L20-L39, L22-L41, L4-L23
.agent/orchestrator/file_writer.py: L4-L23, L5-L24, L3-L22, L6-L25
.agent/orchestrator/kobold_client.py: L17-L36, L22-L41, L2-L21, L16-L35, L14-L33
.agent/orchestrator/page_extractor.py: L23-L42, L21-L40, L25-L44
.agent/orchestrator/patch_applier.py: L8-L27, L5-L24, L6-L25, L7-L26
.agent/orchestrator/playwright_research.py: L17-L36, L7-L26, L9-L28
.agent/orchestrator/prompt_compiler.py: L35-L46
.agent/orchestrator/research_client.py: L1-L20, L63-L82, L30-L49, L61-L80, L42-L61
.agent/orchestrator/response_parser.py: L30-L49, L152-L171, L155-L174, L156-L175, L168-L187
.agent/orchestrator/retry_engine.py: L17-L36, L66-L85, L5-L24, L58-L77, L8-L27
.agent/orchestrator/role_loader.py: L22-L41, L23-L42, L2-L21, L3-L22, L13-L32
.agent/orchestrator/safety_guard.py: L55-L74, L43-L62, L68-L87, L67-L86, L61-L80
.agent/orchestrator/session_router.py: L71-L90, L44-L63, L46-L65, L17-L36, L41-L60
.agent/orchestrator/skill_registry.py: L74-L93, L17-L36, L30-L49, L16-L35, L67-L86
.agent/orchestrator/source_summarizer.py: L7-L17
.agent/orchestrator/state_store.py: L149-L168, L131-L150, L208-L215, L145-L164, L130-L149
.agent/orchestrator/studio_loop.py: L47-L66, L77-L96, L63-L82, L32-L51, L602-L621
.agent/orchestrator/transition_engine.py: L4-L23, L26-L45, L30-L49, L38-L57, L44-L63
.agent/orchestrator/templates/stage_prompt.md: L79-L98, L21-L40, L19-L38, L31-L50
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L38-L57, L86-L95, L1-L17
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L1-L18, L70-L89, L81-L100, L33-L52
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L15-L34, L120-L139, L13-L32
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L87-L106
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L97-L116, L25-L44, L34-L53, L26-L45, L33-L52
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L64-L83
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L22-L41, L20-L39, L31-L50
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L26-L45, L44-L63, L24-L43
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L27-L46
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L25-L44
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L47-L66
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L48-L67
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L17-L36, L64-L77
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L63-L82, L16-L35
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L14-L33, L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L15-L34, L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L2-L21, L5-L24
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L2-L21, L57-L67, L56-L67
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L2-L21, L1-L17
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L2-L21, L5-L24, L1-L17
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L4-L23, L1-L20
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L1-L20, L61-L68
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L17-L36
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L16-L35
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L14-L33, L5-L24, L1-L19, L12-L31
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L4-L23, L1-L18, L16-L35, L18-L37
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L17-L36, L14-L33
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L17-L36, L19-L38
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L74-L93, L53-L72, L42-L61, L82-L101, L44-L63
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L4-L23, L8-L27, L3-L22, L6-L25
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L4-L23, L6-L25
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L23-L42, L27-L46, L1-L19, L24-L43
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L26-L45, L21-L40, L1-L19, L25-L44
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L29-L48, L17-L36, L20-L39, L4-L23, L3-L22
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L25-L44, L20-L39, L4-L23, L112-L128, L3-L22
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L6-L25
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L2-L21
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L108-L127, L97-L116, L35-L54
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L29-L48, L100-L119, L109-L128
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L72-L91, L23-L42, L51-L70, L198-L217, L39-L58
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L231-L250, L310-L329, L41-L60, L166-L185, L132-L151
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L55-L74, L43-L62, L23-L42, L133-L152, L70-L89
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L4-L23, L7-L26, L14-L33, L12-L31
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L2-L21, L11-L30, L9-L28
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L13-L32, L6-L25
.agent/skills/asset_creator_skills.md: L7-L26
.agent/skills/designer_skills.md: L25-L44, L55-L60, L34-L53, L49-L60, L1-L15
.agent/skills/developer_skills.md: L17-L36, L41-L60, L20-L39, L23-L42, L51-L63
.agent/skills/producer_skills.md: L25-L44, L22-L41, L2-L21, L26-L45, L42-L48
.agent/skills/qa_skills.md: L20-L39, L26-L45, L21-L40, L33-L48, L43-L48
.agent/skills/registry.json: L1-L13
.agent/skills/researcher_skills.md: L36-L55, L25-L44, L23-L42, L2-L21, L90-L97
.agent/skills/asset_creator/skill.json: L2-L15
.agent/skills/bug_hunter/SKILL.md: L1-L3
.agent/skills/designer/skill.json: L6-L20, L1-L19, L12-L20, L5-L20, L1-L16
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L4-L15, L2-L15
.agent/skills/researcher/skill.json: L1-L19, L15-L21, L1-L16, L8-L21, L13-L21
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L22-L41, L23-L42, L13-L32, L19-L38, L10-L29
.agent/workflows/bug_hunter.md: L25-L40, L26-L40
.agent/workflows/concept_producer.md: L29-L48, L21-L40, L32-L51, L14-L33, L33-L51
.agent/workflows/debug_dev.md: L14-L33, L11-L30
.agent/workflows/designer.md: L1-L18, L17-L36, L20-L39, L13-L32, L28-L43
.agent/workflows/developer.md: L41-L60, L32-L51, L16-L35, L31-L50, L33-L52
.agent/workflows/qa_tester.md: L20-L39, L46-L60, L19-L38, L42-L60, L14-L33
.agent/workflows/researcher.md: L1-L18, L25-L44, L34-L53, L21-L40, L28-L47
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L29-L48, L1-L20, L41-L60, L77-L96, L54-L73
.agent/workflows/task_template.md: L1-L19, L22-L41, L21-L40, L13-L32, L28-L47
docs/verification/browser_research_mdn_requestanimationframe.md: L40-L53, L28-L47, L22-L41, L31-L50
tests/e2e_loop_test.py: L47-L66, L136-L148, L63-L82, L70-L89, L100-L119
tests/real_browser_research_check.py: L41-L60, L34-L53, L33-L52, L37-L56, L35-L54
tests/test_autonomous_loop.py: L25-L44, L43-L62, L68-L87, L66-L85, L54-L73
tests/test_browser_research_mock.py: L166-L185, L152-L171, L98-L117, L118-L137, L37-L56
tests/test_kobold_client.py: L45-L59, L14-L33, L11-L30, L35-L54
tests/test_repair_prompt.py: L231-L250, L109-L128, L239-L258, L207-L226, L98-L117
tests/test_response_parser.py: L63-L82, L207-L226, L155-L174, L205-L224, L70-L89
tests/test_robustness.py: L32-L51, L37-L56, L42-L61, L48-L67, L76-L95
tests/test_sessions_and_skills.py: L183-L202, L49-L68, L166-L185, L177-L196, L32-L51
tests/fixtures/research_mdn_requestanimationframe.json: L16-L24
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L29-L48, L92-L111, L103-L122, L5-L24, L62-L81
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L71-L90, L55-L74, L166-L185, L4-L23, L84-L103
tests/__pycache__/test_response_parser.cpython-314.pyc: L36-L55, L96-L115, L52-L71, L84-L103, L107-L124
tests/__pycache__/test_robustness.cpython-314.pyc: L1-L19
tools/bootstrap_local_env.py: L57-L76, L52-L71, L61-L80, L70-L89, L58-L77
tools/bundle_project.py: L1-L20, L41-L60
tools/context_culler.py: L36-L55, L17-L36, L16-L35, L18-L37, L19-L38
tools/test_orchestrator.py: L55-L74, L125-L135, L66-L85, L96-L115, L127-L135
tools/verify_clean_runtime.py: L194-L213, L196-L215, L98-L117, L108-L127, L226-L245
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L10-L29, L6-L25

