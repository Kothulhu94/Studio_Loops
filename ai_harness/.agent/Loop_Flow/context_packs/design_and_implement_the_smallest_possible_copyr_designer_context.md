# Context Pack: design_and_implement_the_smallest_possible_copyr / designer

## Feature Goal
Design and implement the smallest possible copyright-safe sci-fi base management prototype slice: room placement data model, worker task queue, and one simple Vitest test. Keep scope tiny. Do not add UI. Do not add dependencies.

## Current Stage
designer

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
--- Context Pruning Map for: ['design', 'implement', 'smallest', 'possible', 'copyright-safe', 'sci-fi', 'base', 'management', 'prototype', 'slice:', 'room', 'placement', 'data', 'designer', 'design_and_implement_the_smallest_possible_copyr_researcher_investigate_the_current_vitest_research_brief.md', 'design_and_implement_the_smallest_possible_copyr_researcher_examine_the__agent_workflows_research_brief.md', 'investigate', 'current', 'vitest', 'configuration'] ---
ai_harness_bundle.txt: L1375-L1394, L1906-L1925, L71-L90, L547-L566, L1343-L1362
HANDOFF_SCHEMA.json: L105-L124, L50-L69, L13-L32, L30-L49, L34-L53
package-lock.json: L484-L503, L1205-L1224, L463-L482, L1239-L1258, L1237-L1256
package.json: L7-L14, L3-L14
tsconfig.json: L8-L14, L6-L14
vitest.config.ts: L1-L8
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L24-L43, L56-L75, L37-L56, L15-L34
.agent/bin/licenses/github.com/atotto/clipboard/LICENSE: L19-L27
.agent/bin/licenses/github.com/fsnotify/fsnotify/LICENSE: L17-L25
.agent/bin/licenses/github.com/godbus/dbus/v5/LICENSE: L16-L25
.agent/bin/licenses/github.com/gorilla/css/scanner/LICENSE: L19-L28
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/CHANGELOG.md: L1-L18
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L109-L128, L322-L341, L228-L247, L286-L305, L188-L207
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither_test.go: L178-L197, L177-L196
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/draw.go: L8-L27, L7-L26, L1-L17, L123-L142, L40-L59
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/error_diffusers.go: L7-L26, L11-L30, L10-L29, L26-L45, L14-L33
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L217-L236, L220-L239, L357-L373, L76-L95, L40-L59
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/pixelmappers.go: L109-L128, L183-L202, L188-L207, L106-L125, L230-L249
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L148-L167, L25-L44, L1-L20
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/special.go: L2-L9
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/examples/gif_image/main.go: L1-L17
.agent/bin/licenses/github.com/microcosm-cc/bluemonday/LICENSE.md: L20-L28
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L24-L43, L56-L75, L37-L56, L15-L34
.agent/bin/licenses/github.com/minio/selfupdate/internal/osext/LICENSE: L19-L27
.agent/bin/licenses/github.com/pkg/browser/LICENSE: L15-L23
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L23-L42, L55-L74, L14-L33, L36-L55
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L23-L42, L55-L74, L14-L33, L36-L55
.agent/bin/licenses/github.com/spf13/pflag/LICENSE: L20-L28
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L24-L43, L56-L75, L37-L56, L15-L34
.agent/bin/licenses/golang.org/x/crypto/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/image/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/mod/semver/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/net/html/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/oauth2/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sync/errgroup/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sys/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/term/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/text/LICENSE: L19-L27
.agent/Loop_Flow/autonomous_studio_expansion_blueprint.md: L11-L17, L9-L17, L10-L17, L12-L17
.agent/Loop_Flow/context_map.json: L15-L29, L19-L29
.agent/Loop_Flow/orchestrator_expansion_blueprint.md: L19-L38, L3-L22, L13-L32, L1-L18, L42-L50
.agent/Loop_Flow/source_index.json: L8-L27, L451-L470, L4-L23, L553-L572, L499-L518
.agent/orchestrator/actions_schema.json: L8-L27, L87-L106
.agent/orchestrator/artifact_store.py: L10-L29, L3-L22, L13-L32
.agent/orchestrator/artifact_validator.py: L103-L122, L1-L20, L184-L203, L26-L45, L2-L21
.agent/orchestrator/browser_research.py: L104-L123, L197-L216, L194-L213, L157-L176, L14-L33
.agent/orchestrator/capability_registry.py: L105-L124, L71-L90, L69-L88, L74-L93, L97-L116
.agent/orchestrator/command_allowlist.json: L6-L25, L12-L31
.agent/orchestrator/command_runner.py: L69-L88
.agent/orchestrator/config.json: L1-L17
.agent/orchestrator/context_compactor.py: L43-L62
.agent/orchestrator/context_pruner.py: L19-L38, L58-L77, L28-L47, L111-L126, L83-L102
.agent/orchestrator/copyright_guard.py: L16-L35, L20-L39, L3-L22, L1-L20, L37-L56
.agent/orchestrator/file_writer.py: L6-L25, L5-L24, L4-L23
.agent/orchestrator/kobold_client.py: L16-L35, L22-L41, L14-L33, L2-L21, L17-L36
.agent/orchestrator/page_extractor.py: L23-L42, L25-L44, L21-L40
.agent/orchestrator/patch_applier.py: L7-L26, L8-L27, L6-L25
.agent/orchestrator/playwright_research.py: L7-L26, L17-L36, L9-L28
.agent/orchestrator/prompt_compiler.py: L35-L46
.agent/orchestrator/research_client.py: L68-L87, L30-L49, L90-L108, L99-L108, L25-L44
.agent/orchestrator/response_parser.py: L30-L49, L154-L173, L152-L171, L151-L170, L168-L187
.agent/orchestrator/retry_engine.py: L50-L69, L8-L27, L58-L77, L17-L36, L66-L85
.agent/orchestrator/role_loader.py: L3-L22, L22-L41, L14-L33, L23-L42, L55-L73
.agent/orchestrator/safety_guard.py: L43-L62, L68-L87, L69-L88, L55-L74, L6-L25
.agent/orchestrator/session_router.py: L19-L38, L16-L35, L43-L62, L45-L64, L71-L90
.agent/orchestrator/skill_registry.py: L16-L35, L30-L49, L74-L93, L17-L36, L67-L86
.agent/orchestrator/source_summarizer.py: L7-L17
.agent/orchestrator/state_store.py: L208-L215, L130-L149, L131-L150, L149-L168, L42-L61
.agent/orchestrator/studio_loop.py: L128-L147, L734-L753, L692-L711, L50-L69, L810-L829
.agent/orchestrator/transition_engine.py: L16-L35, L20-L39, L52-L65, L30-L49, L10-L29
.agent/orchestrator/templates/stage_prompt.md: L19-L38, L79-L98, L31-L50, L21-L40
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L86-L95, L1-L17
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L81-L100, L1-L18, L70-L89
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L13-L32, L15-L34
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L50-L69, L34-L53, L26-L45, L97-L116, L25-L44
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L20-L39, L31-L50, L22-L41
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L24-L43, L44-L63, L26-L45
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L27-L46
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L25-L44
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L47-L66
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L48-L67
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L17-L36, L64-L77
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L16-L35, L63-L82
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19, L14-L33
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20, L15-L34
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L5-L24, L2-L21
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L57-L67, L56-L67, L2-L21
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L17, L2-L21
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L5-L24, L1-L17, L2-L21
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L1-L20, L4-L23
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L61-L68, L1-L20
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L17-L36
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L16-L35
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L14-L33, L1-L19, L5-L24, L12-L31
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L16-L35, L18-L37, L1-L18, L4-L23
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L17-L36, L14-L33
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L17-L36, L19-L38
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L53-L72, L86-L105, L74-L93, L44-L63, L42-L61
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L8-L27, L3-L22, L6-L25, L4-L23
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L6-L25, L4-L23
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L24-L43, L23-L42, L27-L46, L1-L19
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L25-L44, L1-L19, L26-L45, L21-L40
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L20-L39, L3-L22, L8-L27, L10-L29, L28-L47
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L20-L39, L3-L22, L11-L30, L112-L128, L25-L44
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L6-L25
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L2-L21
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L97-L116, L108-L127, L35-L54
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L100-L119, L29-L48, L109-L128
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L111-L130, L142-L161, L23-L42, L198-L217, L51-L70
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L166-L185, L56-L75, L132-L151, L231-L250, L310-L329
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L43-L62, L133-L152, L55-L74, L23-L42, L182-L201
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L14-L33, L12-L31, L4-L23
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L11-L30, L9-L28, L2-L21
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L6-L25, L13-L32
.agent/skills/asset_creator_skills.md: L7-L26
.agent/skills/designer_skills.md: L1-L15, L55-L60, L8-L27, L37-L56, L1-L16
.agent/skills/developer_skills.md: L16-L35, L20-L39, L48-L63, L51-L63, L32-L51
.agent/skills/producer_skills.md: L22-L41, L26-L45, L2-L21, L27-L46, L25-L44
.agent/skills/qa_skills.md: L20-L39, L33-L48, L26-L45, L38-L48, L43-L48
.agent/skills/registry.json: L1-L13
.agent/skills/researcher_skills.md: L7-L26, L69-L88, L2-L21, L40-L59, L25-L44
.agent/skills/asset_creator/skill.json: L2-L15
.agent/skills/designer/skill.json: L5-L20, L6-L20, L1-L16, L12-L20, L1-L17
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L2-L15, L4-L15
.agent/skills/researcher/skill.json: L8-L21
.agent/workflows/asset_creator.md: L19-L38, L13-L32, L22-L41, L10-L29, L23-L42
.agent/workflows/bug_hunter.md: L25-L40, L26-L40
.agent/workflows/concept_producer.md: L29-L48, L21-L40, L14-L33
.agent/workflows/debug_dev.md: L11-L30, L14-L33
.agent/workflows/designer.md: L20-L39, L13-L32, L1-L16, L10-L29, L1-L18
.agent/workflows/developer.md: L16-L35, L32-L51, L27-L46, L33-L52, L41-L60
.agent/workflows/qa_tester.md: L19-L38, L20-L39, L46-L60, L14-L33, L42-L60
.agent/workflows/researcher.md: L25-L44, L28-L47, L21-L40, L15-L34
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L1-L20, L54-L73, L30-L49, L11-L30, L33-L52
.agent/workflows/task_template.md: L28-L47, L21-L40
docs/verification/browser_research_mdn_requestanimationframe.md: L31-L50, L28-L47, L40-L53, L22-L41
tests/e2e_loop_test.py: L19-L38, L16-L35, L105-L124, L101-L120, L13-L32
tests/real_browser_research_check.py: L34-L53, L33-L52, L35-L54
tests/test_autonomous_loop.py: L54-L73, L37-L56, L10-L29, L97-L107, L15-L34
tests/test_browser_research_mock.py: L166-L185, L91-L110, L37-L56, L162-L181, L10-L29
tests/test_kobold_client.py: L11-L30, L45-L59, L14-L33, L35-L54
tests/test_repair_prompt.py: L233-L252, L103-L122, L207-L226, L13-L32, L134-L153
tests/test_response_parser.py: L190-L209, L207-L226, L178-L197, L218-L229, L206-L225
tests/test_robustness.py: L13-L32, L18-L37, L96-L105, L37-L56, L52-L71
tests/test_sessions_and_skills.py: L215-L234, L104-L123, L79-L98, L157-L176, L14-L33
tests/fixtures/research_mdn_requestanimationframe.json: L16-L24
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L103-L122, L91-L110, L88-L107, L62-L81, L5-L24
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L166-L185, L90-L109, L71-L90, L4-L23, L152-L171
tests/__pycache__/test_response_parser.cpython-314.pyc: L84-L103, L103-L122, L101-L120, L88-L107, L102-L121
tests/__pycache__/test_robustness.cpython-314.pyc: L1-L19
tools/bootstrap_local_env.py: L58-L77, L52-L71, L69-L88, L57-L76, L61-L80
tools/bundle_project.py: L1-L20, L41-L60
tools/context_culler.py: L19-L38, L16-L35, L14-L33, L17-L36, L18-L37
tools/test_orchestrator.py: L101-L120, L102-L121, L33-L52, L18-L37, L127-L135
tools/verify_clean_runtime.py: L128-L147, L194-L213, L98-L117, L218-L237, L101-L120
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L10-L29, L6-L25

