# Context Pack: design_and_implement_the_smallest_possible_copyr / concept_producer

## Feature Goal
Design and implement the smallest possible copyright-safe sci-fi base management prototype slice: room placement data model, worker task queue, and one simple Vitest test. Keep scope tiny. Do not add UI. Do not add dependencies.

## Current Stage
concept_producer

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/design_and_implement_the_smallest_possible_copyr_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{}

## Relevant Research Briefs
No research briefs available yet.

## Validation Status
[]

## Pruned Source Context
--- Context Pruning Map for: ['design', 'implement', 'smallest', 'possible', 'copyright-safe', 'sci-fi', 'base', 'management', 'prototype', 'slice:', 'room', 'placement', 'data', 'concept_producer'] ---
ai_harness_bundle.txt: L1549-L1568, L1902-L1921, L1944-L1963, L1953-L1972, L1943-L1962
HANDOFF_SCHEMA.json: L40-L59, L57-L76, L50-L69, L34-L53, L62-L81
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L56-L75, L37-L56, L15-L34
.agent/bin/licenses/github.com/atotto/clipboard/LICENSE: L19-L27
.agent/bin/licenses/github.com/fsnotify/fsnotify/LICENSE: L17-L25
.agent/bin/licenses/github.com/godbus/dbus/v5/LICENSE: L16-L25
.agent/bin/licenses/github.com/gorilla/css/scanner/LICENSE: L19-L28
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/CHANGELOG.md: L1-L18
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L93-L112, L228-L247
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/draw.go: L40-L59, L1-L17, L123-L142, L8-L27, L7-L26
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L40-L59, L220-L239, L357-L373, L76-L95, L217-L236
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/pixelmappers.go: L106-L125, L310-L329, L109-L128, L172-L191, L230-L249
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L148-L167, L25-L44, L1-L20
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/examples/gif_image/main.go: L1-L17
.agent/bin/licenses/github.com/microcosm-cc/bluemonday/LICENSE.md: L20-L28
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L56-L75, L37-L56, L15-L34
.agent/bin/licenses/github.com/minio/selfupdate/internal/osext/LICENSE: L19-L27
.agent/bin/licenses/github.com/pkg/browser/LICENSE: L15-L23
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L14-L33, L55-L74, L36-L55
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L14-L33, L55-L74, L36-L55
.agent/bin/licenses/github.com/spf13/pflag/LICENSE: L20-L28
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L56-L75, L37-L56, L15-L34
.agent/bin/licenses/golang.org/x/crypto/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/image/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/mod/semver/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/net/html/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/oauth2/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sync/errgroup/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/sys/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/term/LICENSE: L19-L27
.agent/bin/licenses/golang.org/x/text/LICENSE: L19-L27
.agent/Loop_Flow/source_index.json: L541-L560, L553-L572, L451-L470, L499-L518
.agent/orchestrator/actions_schema.json: L6-L25, L8-L27, L87-L106
.agent/orchestrator/artifact_store.py: L10-L29, L3-L22, L13-L32
.agent/orchestrator/artifact_validator.py: L152-L171, L159-L178, L184-L203, L103-L122, L2-L21
.agent/orchestrator/browser_research.py: L16-L35, L14-L33, L10-L29, L194-L213, L55-L74
.agent/orchestrator/capability_registry.py: L71-L90, L61-L80, L66-L85, L59-L78, L69-L88
.agent/orchestrator/command_runner.py: L69-L88
.agent/orchestrator/config.json: L1-L17
.agent/orchestrator/context_compactor.py: L43-L62
.agent/orchestrator/context_pruner.py: L113-L126, L61-L80, L111-L126, L58-L77, L83-L102
.agent/orchestrator/copyright_guard.py: L40-L59, L16-L35, L4-L23, L39-L58, L67-L72
.agent/orchestrator/file_writer.py: L6-L25, L4-L23, L5-L24, L2-L21
.agent/orchestrator/kobold_client.py: L16-L35, L14-L33, L2-L21, L17-L36, L22-L41
.agent/orchestrator/page_extractor.py: L21-L40, L23-L42, L25-L44
.agent/orchestrator/patch_applier.py: L6-L25, L4-L23, L8-L27, L7-L26
.agent/orchestrator/playwright_research.py: L9-L28, L17-L36, L7-L26
.agent/orchestrator/research_client.py: L41-L60, L63-L82, L89-L108, L42-L61, L59-L78
.agent/orchestrator/response_parser.py: L10-L29, L135-L154, L156-L175, L172-L191, L154-L173
.agent/orchestrator/retry_engine.py: L50-L69, L66-L85
.agent/orchestrator/role_loader.py: L14-L33, L3-L22, L31-L50, L23-L42, L24-L43
.agent/orchestrator/safety_guard.py: L61-L80, L66-L85, L42-L61, L55-L74, L70-L89
.agent/orchestrator/session_router.py: L16-L35, L14-L33, L10-L29, L28-L47, L51-L70
.agent/orchestrator/skill_registry.py: L16-L35, L30-L49, L17-L36, L67-L86, L48-L67
.agent/orchestrator/source_summarizer.py: L7-L17
.agent/orchestrator/state_store.py: L131-L150, L130-L149
.agent/orchestrator/studio_loop.py: L785-L804, L731-L750, L711-L730, L63-L82, L567-L586
.agent/orchestrator/transition_engine.py: L4-L23, L8-L27, L30-L49, L29-L48, L5-L24
.agent/orchestrator/templates/stage_prompt.md: L21-L40, L79-L98
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L1-L17, L86-L95
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L81-L100, L70-L89, L1-L18
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L13-L32, L15-L34
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L50-L69, L24-L43, L12-L31, L26-L45, L33-L52
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L20-L39, L22-L41
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L24-L43, L26-L45
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L27-L46
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L25-L44
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L47-L66
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L48-L67
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L64-L77
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L63-L82
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19, L14-L33
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L15-L34, L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L4-L23, L5-L24, L2-L21
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L57-L67, L56-L67, L2-L21, L1-L20
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L2-L21, L1-L17
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L2-L21, L1-L17, L5-L24
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L4-L23, L3-L22, L1-L20
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L61-L68, L1-L19, L1-L20
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L19
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L1-L19, L14-L33, L12-L31, L5-L24
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L16-L35, L4-L23, L18-L37, L1-L18
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L14-L33, L17-L36
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L17-L36, L19-L38
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L82-L101, L74-L93
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L6-L25, L4-L23, L3-L22, L8-L27
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L6-L25, L4-L23, L3-L22
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L1-L19, L23-L42, L27-L46, L24-L43
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L20-L39, L1-L19, L26-L45, L21-L40, L25-L44
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L10-L29, L8-L27, L3-L22, L20-L39, L29-L48
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L11-L30, L3-L22, L112-L128, L6-L25, L25-L44
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L6-L25
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L2-L21
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L97-L116
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L100-L119
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L39-L58, L198-L217, L111-L130, L23-L42, L142-L161
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L132-L151, L41-L60, L166-L185, L24-L43, L310-L329
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L133-L152, L23-L42, L43-L62, L182-L201
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L4-L23, L12-L31
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L9-L28, L2-L21, L1-L20
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L6-L25, L13-L32
.agent/skills/asset_creator_skills.md: L7-L26
.agent/skills/designer_skills.md: L40-L59, L1-L15, L11-L30, L55-L60, L34-L53
.agent/skills/developer_skills.md: L16-L35, L48-L63, L58-L63, L42-L61, L51-L63
.agent/skills/producer_skills.md: L27-L46, L43-L48, L42-L48, L2-L21, L26-L45
.agent/skills/qa_skills.md: L21-L40, L20-L39
.agent/skills/registry.json: L1-L13
.agent/skills/researcher_skills.md: L40-L59, L36-L55, L2-L21, L7-L26, L69-L88
.agent/skills/asset_creator/skill.json: L2-L15
.agent/skills/designer/skill.json: L6-L20, L12-L20, L1-L17, L5-L20, L14-L20
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L2-L15, L4-L15
.agent/skills/producer/skill.json: L1-L19
.agent/skills/researcher/skill.json: L8-L21
.agent/workflows/asset_creator.md: L10-L29, L19-L38, L23-L42, L13-L32, L22-L41
.agent/workflows/bug_hunter.md: L26-L40, L25-L40
.agent/workflows/concept_producer.md: L14-L33, L29-L48
.agent/workflows/debug_dev.md: L11-L30, L14-L33
.agent/workflows/designer.md: L10-L29, L20-L39, L24-L43, L12-L31, L13-L32
.agent/workflows/developer.md: L16-L35, L32-L51, L31-L50, L41-L60, L35-L54
.agent/workflows/qa_tester.md: L46-L60
.agent/workflows/researcher.md: L28-L47
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L11-L30, L80-L96, L30-L49, L41-L60, L54-L73
.agent/workflows/task_template.md: L21-L40, L28-L47
docs/verification/browser_research_mdn_requestanimationframe.md: L40-L53, L28-L47, L31-L50, L22-L41
tests/e2e_loop_test.py: L125-L144, L16-L35, L11-L30, L136-L148, L19-L38
tests/real_browser_research_check.py: L33-L52, L35-L54, L34-L53
tests/test_autonomous_loop.py: L54-L73, L10-L29, L37-L56, L15-L34
tests/test_browser_research_mock.py: L152-L171, L39-L58, L10-L29, L27-L46, L119-L138
tests/test_kobold_client.py: L11-L30, L14-L33, L35-L54, L45-L59
tests/test_repair_prompt.py: L134-L153, L17-L36, L139-L158, L18-L37, L13-L32
tests/test_response_parser.py: L190-L209, L19-L38, L178-L197, L218-L229, L37-L56
tests/test_robustness.py: L28-L47, L42-L61, L76-L95, L32-L51, L18-L37
tests/test_sessions_and_skills.py: L103-L122, L19-L38, L100-L119, L111-L130, L124-L143
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L62-L81, L103-L122, L5-L24
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L152-L171, L16-L35, L4-L23, L117-L136, L99-L118
tests/__pycache__/test_response_parser.cpython-314.pyc: L10-L29, L88-L107, L107-L124, L22-L41, L101-L120
tests/__pycache__/test_robustness.cpython-314.pyc: L1-L19
tools/bootstrap_local_env.py: L69-L88, L70-L89
tools/bundle_project.py: L41-L60
tools/context_culler.py: L16-L35, L14-L33, L19-L38, L36-L55, L18-L37
tools/test_orchestrator.py: L89-L108, L121-L135, L71-L90, L52-L71, L62-L81
tools/verify_clean_runtime.py: L108-L127, L159-L178, L249-L268, L103-L122, L111-L130
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L6-L25, L10-L29

